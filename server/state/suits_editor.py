import flask
from server.api_utils import get_field, make_get_json_route, make_post_json_route

import dat1lib.types.sections.config.serialized
import dat1lib.types.sections.config.references
import io
import os
import struct

BLANK_PIC = bytes.fromhex("89504E470D0A1A0A0000000D49484452000000120000000D01030000009E80AC5A00000003504C5445F2F2F264038A6B0000000B4944415408D76320030000003400019232F3470000000049454E44AE426082")

class SuitsEditor(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/suits_editor/make", self.make_editor)
		make_post_json_route(app, "/api/suits_editor/refresh_icons", self.refresh_icons)
		make_get_json_route(app, "/api/suits_editor/icon", self.get_icon, False)

	def make_editor(self):
		return self.get_suits_editor()

	def refresh_icons(self):
		return self.cache_icons()

	def get_icon(self):
		aid = get_field(flask.request.args, "aid")
		return self.get_cached_icon_png(aid)

	# internal

	def boot(self):
		os.makedirs(".cache/suits/", exist_ok=True)

	#

	def _get_progression_config(self):
		aid = 0x9C9C72A303FCFA30 # configs/system/system_progression.config
		toc = self.state.toc_loader.toc
		entry = toc.get_asset_entries_by_assetid(aid, True)
		data, asset = self.state._read_asset(entry[0].index)
		return asset

	def get_suits_editor(self):
		result = {
			"suits": [],
			"references": []
		}

		asset = self._get_progression_config()
		s = asset.dat1.get_section(dat1lib.types.sections.config.serialized.ConfigContentSection.TAG)
		j = s.root
		for techlist in j["TechWebLists"]:
			if "Description" not in techlist or techlist["Description"] != "Suits":
				continue

			result["suits"] = techlist["TechWebItems"]
			break

		s = asset.dat1.get_section(dat1lib.types.sections.config.references.ReferencesSection.TAG)
		if s is not None:
			result["references"] = [("{:016X}".format(x[0]), asset.dat1.get_string(x[1])) for x in s.entries]

		return result

	#

	def _get_cached_icon_path(self, aid, index):
		return ".cache/suits/{}.{:08X}.png".format(aid, self.state.thumbnails._get_asset_metahash(index))

	def get_cached_icon_png(self, aid):
		node = self.state.toc_loader._get_node_by_aid(aid)
		aid, variants = node[0], node[1]
		for index, archive_index in variants:
			fn = self._get_cached_icon_path(aid, index)
			if os.path.exists(fn):
				f = open(fn, "rb")
				return (flask.send_file(f, mimetype='image/png', max_age=0), 200)

		return (flask.send_file(io.BytesIO(BLANK_PIC), mimetype='image/png', max_age=0), 200)

	#

	def _normalize_path(self, path):
		return path.lower().replace('\\', '/')

	def cache_icons(self):
		editor = self.get_suits_editor()
		result = {}

		references_map = {}
		for aid, path in editor["references"]:
			references_map[self._normalize_path(path)] = aid

		for s in editor["suits"]:
			if "PreviewImage" in s:
				aid = references_map[self._normalize_path(s["PreviewImage"])]
				result[aid] = self._cache_icon(aid)

		return {"icons": result}

	def _cache_icon(self, aid):
		node = self.state.toc_loader._get_node_by_aid(aid)
		aid, variants = node[0], node[1]

		for index, archive_index in variants:
			if self._try_caching_icon(aid, index):
				return True

		return False

	def _try_caching_icon(self, aid, index):
		try:
			fn = self._get_cached_icon_path(aid, index)
			data, asset = self.state._get_asset_by_index(index)

			if isinstance(asset, dat1lib.types.autogen.Texture):
				img = self.state.textures._load_dds_mipmap(asset, None, 0)
				if img is None:
					return False

				img.save(fn)
				return True
		except:
			print(traceback.format_exc())

		return False
