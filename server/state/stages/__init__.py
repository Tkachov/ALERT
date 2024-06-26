# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import flask
from server.api_utils import get_field, make_get_json_route, make_post_json_route

import io
import os
import os.path
import platform
import re
import subprocess

from server.state.stages.stage import Stage
from server.state.stages.smpcmod_importer import StagesModImporter
from server.state.stages.suit_importer import StagesSuitImporter
from server.state.stages.suit_exporter import StagesSuitExporter

class Stages(object):
	def __init__(self, state):
		self.state = state
		self.smpcmod_importer = StagesModImporter(self)
		self.suit_importer = StagesSuitImporter(self)
		self.suit_exporter = StagesSuitExporter(self)
		self.reboot()

	def reboot(self):
		self.stages = {}

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/stages/refresh", self.refresh_stages)
		make_post_json_route(app, "/api/stages/open_explorer", self.open_explorer)
		make_post_json_route(app, "/api/stages/add_asset", self.stage_asset)
		make_post_json_route(app, "/api/stages/add_directory", self.stage_directory)
		make_post_json_route(app, "/api/stages/import_smpcmod", self.import_smpcmod)
		make_post_json_route(app, "/api/stages/import_suit", self.import_suit)
		make_post_json_route(app, "/api/stages/make_export_suit", self.make_export_suit)
		make_post_json_route(app, "/api/stages/export_suit", self.export_suit)
		make_get_json_route(app, "/api/stages/exported_suit", self.get_exported_suit, False)

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

	def import_smpcmod(self):
		rq = flask.request
		stage = get_field(rq.form, "stage")
		smpcmod = rq.files["smpcmod"].read()
		return self.smpcmod_importer.import_smpcmod(io.BytesIO(smpcmod), stage)

	def import_suit(self):
		rq = flask.request
		stage = get_field(rq.form, "stage")
		suit = rq.files["suit"].read()
		return self.suit_importer.import_suit(io.BytesIO(suit), stage)

	def make_export_suit(self):
		rq = flask.request
		stage = get_field(rq.form, "stage")
		return self.suit_exporter.make_export_suit(stage)

	def export_suit(self):
		rq = flask.request
		return self.suit_exporter.export_suit(rq.form)

	def get_exported_suit(self):
		rq = flask.request
		filename = get_field(rq.args, "filename")
		return flask.send_file(self.suit_exporter.get_exported_suit(filename), as_attachment=True, download_name=filename, mimetype='application/octet-stream')

	# internal

	def boot(self):
		os.makedirs("stages/", exist_ok=True)

		for fn in os.listdir("stages/"):
			full_fn = os.path.join("stages/", fn)
			if os.path.isdir(full_fn):
				self.stages[fn] = Stage(full_fn)

		self.suit_exporter.boot()

	def get_asset_variants_locators(self, stage, aid):
		if stage not in self.stages:
			raise Exception("Bad stage")

		return self.stages[stage].get_asset_variants_locators(stage, aid)

	def get_assets_under_path(self, stage, path):
		if stage not in self.stages:
			raise Exception("Bad stage")

		return self.stages[stage].get_assets_under_path(self.state, stage, path)

	def get_stage(self, stage, create_if_needed=True): # => (Stage, newly_created:bool)
		if stage in self.stages:
			return (self.stages[stage], False)
		
		if not create_if_needed:
			return (None, False)

		fn = os.path.join("stages/", stage)
		os.makedirs(fn, exist_ok=True)
		self.stages[stage] = Stage(fn)
		return (self.stages[stage], True)

	#

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
			return self._stage_asset_from_stage(locator, dst_stage_object, all_spans)

		aid = locator.asset_id
		path = aid
		if aid in self.state.toc_loader._known_paths:
			path = self.state.toc_loader._known_paths[aid]

		if all_spans:
			locators = self.state.get_asset_variants_locators("", aid)
			for l in locators:
				dst_stage_object.stage_asset_from_toc(path, self.state.locator(l), self.state)
		else:
			dst_stage_object.stage_asset_from_toc(path, locator, self.state)

		return True

	def _stage_asset_from_stage(self, locator, dst_stage_object, all_spans):
		src_stage = locator.stage
		path = locator.asset_path
		aid = locator.asset_id
		if path is None:
			path = aid

		if src_stage not in self.stages:
			raise Exception("Bad stage")

		if all_spans:
			locators = self.get_asset_variants_locators(src_stage, aid)	
			for l in locators:
				dst_stage_object.stage_asset_from_stage(path, self.state.locator(l), self.state)
		else:
			dst_stage_object.stage_asset_from_stage(path, locator, self.state)

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
