import flask
from server.api_utils import get_field, make_post_json_route

import dat1lib
import dat1lib.crc64 as crc64
import dat1lib.types.toc
import dat1lib.types.autogen
import io
import os
import os.path
import platform
import re
import subprocess

def normalize_path(path):
	return path.lower().replace('\\', '/').strip()

class Stage(object):
	def __init__(self, path):
		self.path = path
		self.reload()

	def reload(self):
		self.tree = {}
		self.aid_to_path = {}
		self.spans = []

		for fn in os.listdir(self.path):
			full_fn = os.path.join(self.path, fn)
			if os.path.isdir(full_fn):
				self.add_span(fn, full_fn)

	def _insert_path(self, path, aid):
		if aid in self.aid_to_path:
			return

		self.aid_to_path[aid] = path

		parts = path.split("/")
		dirs, file = parts[:-1], parts[-1]
		
		node = self.tree
		for d in dirs:
			if d not in node:
				node[d] = {}
			node = node[d]

		node[file] = [aid, []]

	def _add_index_to_tree(self, aid, asset_info):
		path = self.aid_to_path[aid]
		parts = path.split("/")
		dirs, file = parts[:-1], parts[-1]
		
		node = self.tree
		for d in dirs:
			if d not in node:
				node[d] = {}
			node = node[d]

		node[file][1] += [asset_info]

	def add_span(self, span_name, path):
		self.spans += [span_name]

		dirs = [""]
		while len(dirs) > 0:
			current_dir = dirs[0]
			dirs = dirs[1:]

			full_dir = os.path.join(path, current_dir)
			for fn in os.listdir(full_dir):
				full_fn = os.path.join(full_dir, fn)
				aid_fn = os.path.join(current_dir, fn)
				if os.path.isdir(full_fn):
					dirs += [aid_fn]
				else:
					if current_dir == "" and len(fn) == 16 and re.match("^[A-Fa-f0-9]{16}$", fn):
						aid_fn = fn.upper()
						aid = aid_fn
					else:
						aid_fn = normalize_path(aid_fn)
						aid = "{:016X}".format(crc64.hash(aid_fn))
					self._insert_path(aid_fn, aid)
					asset_info = [span_name, 0, os.path.getsize(full_fn)]
					self._add_index_to_tree(aid, asset_info)

	def _get_node_by_aid(self, aid):
		path = self.aid_to_path[aid]
		parts = path.split("/")
		dirs, file = parts[:-1], parts[-1]
		
		node = self.tree
		for d in dirs:
			if d not in node:
				node[d] = {}
			node = node[d]

		return node[file]

	def _get_span(self, span_index):
		# TODO: span mappings
		return "{}".format(span_index)

	def stage_asset(self, path, locator, state):
		# TODO: maintain correct structs state
		real_path = os.path.join(self.path, self._get_span(locator.span), path)
		asset_data = state.get_asset_data(locator)

		dir_path = os.path.dirname(real_path)
		os.makedirs(dir_path, exist_ok=True)

		f = open(real_path, "wb")
		f.write(asset_data)
		f.close()

#

class Stages(object):
	def __init__(self, state):
		self.state = state
		self.reboot()

	def reboot(self):
		self.stages = {}

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/stages/refresh", self.refresh_stages)
		make_post_json_route(app, "/api/stages/open_explorer", self.open_explorer)
		make_post_json_route(app, "/api/stages/add_asset", self.stage_asset)
		make_post_json_route(app, "/api/stages/add_directory", self.stage_directory)

	def refresh_stages(self):
		self.reboot()
		self.boot()
		return self.get_boot_info()

	def open_explorer(self):
		stage = get_field(flask.request.form, "stage")
		path = get_field(flask.request.form, "path")
		span = get_field(flask.request.form, "span")

		return {"success": self._open_explorer(stage, path, span)}

	def stage_asset(self):
		stage = get_field(flask.request.form, "stage")
		locator = get_field(flask.request.form, "locator")
		all_spans = (get_field(flask.request.form, "all_spans") == "true")
		return {"success": self._stage_asset(stage, locator, all_spans)}

	def stage_directory(self):
		stage = get_field(flask.request.form, "stage")
		path = get_field(flask.request.form, "path")
		return self._stage_directory(stage, path)

	# internal

	def boot(self):
		os.makedirs("stages/", exist_ok=True)

		for fn in os.listdir("stages/"):
			full_fn = os.path.join("stages/", fn)
			if os.path.isdir(full_fn):
				self.stages[fn] = Stage(full_fn)

	def _open_explorer(self, stage, path, span):
		if platform.system() != "Windows":
			raise Exception("Bad platform")

		if stage is None or stage == "" or stage not in self.stages:
			raise Exception("Bad stage")

		s = self.stages[stage]
		path_to_open = None
		operation = "explore"

		if span is None or span == "":
			if path == "":
				path_to_open = os.path.join("stages/", stage, "")
			else:
				# looking for a directory
				found = False
				for sp in s.spans:
					d = os.path.join("stages/", stage, sp, path, "")
					if os.path.isdir(d):
						path_to_open = d
						found = True
						break

				if not found:
					raise Exception("Bad path")
		else:
			if span not in s.spans:
				raise Exception("Bad span")

			# looking for a file
			p = os.path.join("stages/", stage, span, path)
			if os.path.isfile(p):
				path_to_open = p
				operation = "select"
			else:
				raise Exception("Bad path")

		if path_to_open is not None:
			if operation == "select":
				subprocess.Popen("explorer /select,\"{}\"".format(os.path.abspath(path_to_open)))
			else:
				os.startfile(path_to_open, operation)
			return True

		return False

	def _stage_asset(self, dst_stage, locator, all_spans):
		locator = self.state.locator(locator)

		dst_stage_object = None
		if dst_stage in self.stages:
			dst_stage_object = self.stages[dst_stage]
		else:
			fn = os.path.join("stages/", dst_stage)
			os.makedirs(fn, exist_ok=True)
			dst_stage_object = Stage(fn)

		if locator.stage is not None:
			raise Exception("Bad stage") # TODO: reassess this later

		aid = locator.asset_id
		path = aid
		if aid in self.state.toc_loader._known_paths:
			path = self.state.toc_loader._known_paths[aid]

		if all_spans:
			locators = self.state.get_asset_variants_locators("", aid)
			for l in locators:
				dst_stage_object.stage_asset(path, self.state.locator(l), self.state)
		else:
			dst_stage_object.stage_asset(path, locator, self.state)

		return True

	def _stage_directory(self, dst_stage, path):
		parts = path.split("/")
		
		node = self.state.toc_loader.tree
		for p in parts:
			if p == "":
				continue
			if p not in node:
				node = None
				break
			node = node[p]

		results = {}
		if node is not None:
			for k in node:
				if isinstance(node[k], list):
					aid = node[k][0]
					try:
						results[aid] = self._stage_asset(dst_stage, "/0/" + aid, True)
					except:
						results[aid] = False

		return {"success": True, "assets": results}

	#

	def get_boot_info(self):
		result = {}
		for s in self.stages:
			result[s] = {"tree": self.stages[s].tree}

		return {"stages": result}
