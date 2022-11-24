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

	def refresh_stages(self):
		self.reboot()
		self.boot()
		return self.get_boot_info()

	def open_explorer(self):
		stage = get_field(flask.request.form, "stage")
		path = get_field(flask.request.form, "path")
		span = get_field(flask.request.form, "span")

		return {"success": self._open_explorer(stage, path, span)}

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

	#

	def get_boot_info(self):
		result = {}
		for s in self.stages:
			result[s] = {"tree": self.stages[s].tree}

		return {"stages": result}
