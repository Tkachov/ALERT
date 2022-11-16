import bisect
import dat1lib
import flask
import io
import os.path

import server.state.assets
import server.state.configs_editor
import server.state.models_viewer
import server.state.sections_editor
import server.state.sections_viewer
import server.state.suits_editor
import server.state.textures
import server.state.thumbnails
import server.state.toc_loader
from server.api_utils import get_int, get_field, make_get_json_route, make_post_json_route

#

import string

def is_hex(s):
	return all(c in string.hexdigits for c in s)

class Locator(object):
	def __init__(self, s):
		self.path = s
		self.is_archived = False
		self.stage = ""
		self.span = ""
		self.asset_path = ""
		self.asset_id = ""
		self.is_valid = False

		if len(s) > 0:
			if s[0] == '/':
				self.is_archived = True
				self.stage = None

				i = s.find('/', 1)
				if i != -1:
					self.span = int(s[1:i])
					self.asset_path = None
					self.asset_id = s[i+1:]
					self.is_valid = True
			else:
				i1 = s.find('/')
				i2 = s.find('/', i1+1)
				if i1 != -1 and i2 != -1:
					self.stage = s[:i1]
					self.span = s[i1+1:i2]
					self.asset_path = s[i2+1:]
					if len(self.asset_path) == 16 and is_hex(self.asset_path):
						self.asset_path = None
						self.asset_id = s[i2+1:]
					else:	
						self.asset_id = "{:016X}".format(dat1lib.crc64.hash(self.asset_path))
					self.is_valid = True

	def __str__(self):
		return self.path

#

class State(object):
	def __init__(self, app):
		self.toc_loader = server.state.toc_loader.TocLoader(self)
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
		self.suits_editor.make_api_routes(app)
		self.textures.make_api_routes(app)
		self.thumbnails.make_api_routes(app)

	def boot(self):
		toc_path = get_field(flask.request.form, "toc_path")

		self.toc_loader.load_toc(toc_path)
		self.suits_editor.boot()
		self.textures.boot()
		self.thumbnails.boot()

		return self.toc_loader.get_boot_info()

	# common state methods

	def _read_asset(self, index):
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

	def _get_asset_by_index(self, index):
		if self.currently_extracted_asset_index == index:
			return self.currently_extracted_asset_data, self.currently_extracted_asset
		
		return self._read_asset(index)

	def _get_asset_name(self, index):
		s = self.toc_loader.toc.get_assets_section()
		aid = "{:016X}".format(s.ids[index])
		if aid in self.toc_loader._known_paths:
			return os.path.basename(self.toc_loader._known_paths[aid])
		return aid

	def extract_asset(self, index):
		# TODO: what if I want to force reload?
		s = self.toc_loader.toc.get_sizes_section()
		sz = s.entries[index].value

		if self.currently_extracted_asset_index == index:
			return self.currently_extracted_asset, sz, None

		data, obj = self._read_asset(index)
		self.currently_extracted_asset = obj
		self.currently_extracted_asset_index = index
		self.currently_extracted_asset_data = data

		s = self.toc_loader.toc.get_assets_section()
		aid = "{:016X}".format(s.ids[index])
		made_thumbnail = self.thumbnails._try_making_thumbnail(aid, index)
		thumbnail = aid if made_thumbnail else None

		return self.currently_extracted_asset, sz, thumbnail

	def extract_asset_loc(self, locator):
		if not isinstance(locator, Locator):
			locator = self.locator(locator)

		data, asset = self.get_asset(locator)

		aid = locator.asset_id # TODO: stage appended here?
		# made_thumbnail = self.thumbnails._try_making_thumbnail(aid, index)
		made_thumbnail = False # TODO
		thumbnail = aid if made_thumbnail else None

		return asset, thumbnail

	def _get_asset_by_locator(self, locator):
		return self.get_asset(locator)

	def _get_asset_name_loc(self, locator):
		if not isinstance(locator, Locator):
			locator = self.locator(locator)

		if not locator.is_archived:
			return os.path.basename(locator.path)

		aid = locator.asset_id
		if aid in self.toc_loader._known_paths:
			return os.path.basename(self.toc_loader._known_paths[aid])

		return aid

	#

	def locator(self, s):
		return Locator(s)

	def get_asset_data(self, locator):
		if not isinstance(locator, Locator):
			locator = self.locator(locator)

		if not locator.is_valid:
			raise Exception("Invalid Locator passed: {}".format(locator))

		if not locator.is_archived:
			f = open(os.path.join("stages/", locator.path), "rb")
			data = f.read()
			f.close()

			return data

		# extract data from toc

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

		try:
			data = toc.extract_asset(i)
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

		return data

	def get_asset(self, locator):
		data = self.get_asset_data(locator)

		d = io.BytesIO(data)
		asset = dat1lib.read(d, try_unknown=False)

		return data, asset
