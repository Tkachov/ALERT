import bisect
import copy
import dat1lib
import dat1lib.types.dat1
import flask
import io
import os.path

import server.state.assets
import server.state.configs_editor
import server.state.models_viewer
import server.state.sections_editor
import server.state.sections_viewer
import server.state.stages
import server.state.suits_editor
import server.state.textures
import server.state.thumbnails
import server.state.toc_loader
from server.api_utils import get_int, get_field, make_get_json_route, make_post_json_route
from server.state.types.locator import Locator
from server.state.types.headless_dat1 import HeadlessDAT1

class State(object):
	def __init__(self, app):
		self.toc_loader = server.state.toc_loader.TocLoader(self)
		self.stages = server.state.stages.Stages(self)

		self.assets = server.state.assets.Assets(self)
		self.configs_editor = server.state.configs_editor.ConfigsEditor(self)
		self.models_viewer = server.state.models_viewer.ModelsViewer(self)
		self.sections_editor = server.state.sections_editor.SectionsEditor(self)
		self.sections_viewer = server.state.sections_viewer.SectionsViewer(self)
		self.suits_editor = server.state.suits_editor.SuitsEditor(self)
		self.textures = server.state.textures.Textures(self)
		self.thumbnails = server.state.thumbnails.Thumbnails(self)

		self.reboot()
		self.make_api_routes(app)

	def reboot(self):
		self.toc_loader.reboot()
		self.stages.reboot()

		self.currently_extracted_asset = None
		self.currently_extracted_asset_index = None
		self.currently_extracted_asset_data = None

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/boot", self.boot)

		self.assets.make_api_routes(app)
		self.configs_editor.make_api_routes(app)
		self.models_viewer.make_api_routes(app)
		self.sections_editor.make_api_routes(app)
		self.sections_viewer.make_api_routes(app)
		self.stages.make_api_routes(app)
		self.suits_editor.make_api_routes(app)
		self.textures.make_api_routes(app)
		self.thumbnails.make_api_routes(app)

	def boot(self):
		toc_path = get_field(flask.request.form, "toc_path")

		self.toc_loader.load_toc(toc_path)
		self.stages.boot()
		self.suits_editor.boot()
		self.textures.boot()
		self.thumbnails.boot()

		tlbi = self.toc_loader.get_boot_info()
		sbi = self.stages.get_boot_info()
		return {
			"toc": tlbi["toc"],
			"stages": sbi["stages"]
		}

	# common state methods

	def locator(self, s):
		if not isinstance(s, Locator):
			return Locator(s)
		return s

	def get_asset_with_thumbnail(self, locator):
		locator = self.locator(locator)

		data, asset = self.get_asset(locator)

		taid = "{}_{}".format("" if locator.stage is None else locator.stage, locator.asset_id)
		made_thumbnail = self.thumbnails._try_making_thumbnail(locator, data, asset)
		thumbnail = taid if made_thumbnail else None

		return asset, thumbnail

	def get_asset(self, locator):
		data = self.get_asset_data(locator)

		d = io.BytesIO(data)
		asset = dat1lib.read(d, try_unknown=False)

		if isinstance(asset, dat1lib.types.dat1.DAT1):
			asset = HeadlessDAT1(asset)

		return data, asset

	def get_asset_data(self, locator):
		locator = self.locator(locator)

		if not locator.is_valid:
			raise Exception("Invalid Locator passed: {}".format(locator))

		if not locator.is_archived:
			path = os.path.join("stages/", locator.path)
			if not os.path.exists(path):
				path = os.path.join("stages/", locator.stage, locator.span, locator.asset_id)

			f = open(path, "rb")
			data = f.read()
			f.close()

			return data

		# extract data from toc

		toc = self.toc_loader.toc
		i = self._get_archived_asset_index(locator)

		try:
			return toc.extract_asset(i)
		except Exception as e:
			error_msg = "{}".format(e)

			if "Errno 2" in error_msg and "No such file or directory" in error_msg:
				ri = len(error_msg)-1
				while ri >= 0:
					if error_msg[ri] == '/' or error_msg[ri] == '\\':
						break
					ri -= 1

				raise Exception("missing archive '{}".format(error_msg[ri+1:]))

			raise

	def _get_archived_asset_index(self, locator):
		locator = self.locator(locator)

		toc = self.toc_loader.toc
		spans_section = toc.get_spans_section()
		span = spans_section.entries[locator.span]

		int_aid = int(locator.asset_id, 16)
		assets_section = toc.get_assets_section()
		ids = assets_section.ids
		hi = span.asset_index + span.count
		i = bisect.bisect_left(ids, int_aid, span.asset_index, hi)
		if i >= hi or ids[i] != int_aid:
			raise Exception("{} not found in span#{}".format(locator.asset_id, locator.span))

		return i

	def get_asset_basename(self, locator):
		if not isinstance(locator, Locator):
			locator = self.locator(locator)

		if not locator.is_archived:
			return os.path.basename(locator.path)

		aid = locator.asset_id
		if aid in self.toc_loader._known_paths:
			return os.path.basename(self.toc_loader._known_paths[aid])

		return aid

	#

	def get_asset_variants_locators(self, stage, aid):
		if stage != "":
			return self.stages.get_asset_variants_locators(stage, aid)

		_, variants = self.toc_loader._get_node_by_aid(aid)
		return ["/{}/{}".format(v[0], aid) for v in variants]

	def _make_hd_locator(self, locator):
		locator = self.locator(locator)

		if locator.stage is None:
			hd_locator = copy.deepcopy(locator)
			hd_locator.span = 1
			
			return hd_locator

		hd_locator = None
		all_variants = self.get_asset_variants_locators(locator.stage, locator.asset_id)
		needle_span = self.stages.stages[locator.stage]._get_span(1)
		for v in all_variants:
			variant_locator = self.locator(v)
			if variant_locator.span == locator.span:
				continue
			if hd_locator is None:
				hd_locator = variant_locator
			else:
				if hd_locator.span != needle_span and variant_locator.span == needle_span:
					hd_locator = variant_locator

		if hd_locator is None:
			raise Exception("HD asset not found")

		return hd_locator

	#

	def _read_asset(self, index): # TODO: suits_editor.py uses this -- once it has locators/stages support, this can be removed
		data = None

		try:
			data = self.toc_loader.toc.extract_asset(self.toc_loader.toc.get_asset_entry_by_index(index))
		except Exception as e:
			error_msg = "{}".format(e)

			if "Errno 2" in error_msg and "No such file or directory" in error_msg:
				ri = len(error_msg)-1
				while ri >= 0:
					if error_msg[ri] == '/' or error_msg[ri] == '\\':
						break
					ri -= 1

				raise Exception("missing archive '{}".format(error_msg[ri+1:]))

			raise

		d = io.BytesIO(data)
		obj = dat1lib.read(d, try_unknown=False)

		return data, obj
