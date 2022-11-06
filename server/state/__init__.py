import dat1lib
import flask
import io
import os.path

import server.state.assets
import server.state.models_viewer
import server.state.sections_editor
import server.state.sections_viewer
import server.state.textures
import server.state.thumbnails
import server.state.toc_loader
from server.api_utils import get_int, get_field, make_get_json_route, make_post_json_route

class State(object):
	def __init__(self, app):
		self.toc_loader = server.state.toc_loader.TocLoader(self)
		self.assets = server.state.assets.Assets(self)
		self.models_viewer = server.state.models_viewer.ModelsViewer(self)
		self.sections_editor = server.state.sections_editor.SectionsEditor(self)
		self.sections_viewer = server.state.sections_viewer.SectionsViewer(self)
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
		self.models_viewer.make_api_routes(app)
		self.sections_editor.make_api_routes(app)
		self.sections_viewer.make_api_routes(app)
		self.textures.make_api_routes(app)
		self.thumbnails.make_api_routes(app)

	def boot(self):
		# parse request

		toc_path = get_field(flask.request.form, "toc_path")

		# work

		self.toc_loader.load_toc(toc_path)
		self.textures.boot()
		self.thumbnails.boot()

		# compose response

		toc = self.toc_loader.toc
		archives = toc.get_archives_section()
		assets = toc.get_assets_section()

		return {"toc": {
			"archives": len(archives.archives),
			"assets": len(assets.ids),
			"tree": self.toc_loader.tree,
			"assets_map": self.toc_loader.hashes,
			"archives_map": self.toc_loader.archives
		}}

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
