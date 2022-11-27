import flask
from server.api_utils import get_field, make_get_json_route, make_post_json_route

import dat1lib.types.autogen
import io
import os
import os.path
import platform
import struct
import subprocess
import traceback
import zlib
from PIL import Image

DEBUG_DDS = False

class Thumbnails(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/thumbnails/list", self.list_thumbnails)
		make_get_json_route(app, "/api/thumbnails/png", self.get_png, False)

	def list_thumbnails(self):
		stage = get_field(flask.request.form, "stage")
		path = get_field(flask.request.form, "path")
		return {"list": self.get_thumbnails_list(stage, path)}

	def get_png(self):
		stage = get_field(flask.request.args, "stage")
		aid = get_field(flask.request.args, "aid")
		return self._get_thumbnail(stage, aid)

	# internal

	def boot(self):
		os.makedirs(".cache/thumbnails/", exist_ok=True)

	def _get_asset_metahash(self, locator):
		locator = self.state.locator(locator)
		
		if locator.stage is not None:
			checksum = 0
			try:
				full_fn = "stages/" + locator.path
				if os.path.isfile(full_fn):
					f = open(full_fn, "rb")
					checksum = zlib.crc32(f.read(), checksum)
					f.close()
			except:
				pass
			return checksum

		index = self.state._get_archived_asset_index(locator)
		toc = self.state.toc_loader.toc
		assets_section = toc.get_assets_section()
		archives_section = toc.get_archives_section()
		offsets_section = toc.get_offsets_section()
		sizes_section = toc.get_sizes_section()
		archive_index = offsets_section.entries[index].archive_index
		checksum = zlib.crc32(archives_section.archives[archive_index].filename, 0)
		checksum = zlib.crc32(struct.pack("<QII", assets_section.ids[index], offsets_section.entries[index].offset, sizes_section.entries[index].value), checksum)
		return checksum

	def _get_thumbnail_path(self, locator):
		locator = self.state.locator(locator)
		prefix = "{}{}".format("" if locator.stage is None else locator.stage, "" if locator.stage is None else "_")
		return ".cache/thumbnails/{}{}.{:08X}.png".format(prefix, locator.asset_id, self._get_asset_metahash(locator))

	def get_thumbnails_list(self, stage, path):
		parts = path.split("/")

		if stage != "":
			result = []
			locators = self.state.stages.get_assets_under_path(stage, path)
			for l in locators:
				l = self.state.locator(l)
				fn = self._get_thumbnail_path(l)
				if os.path.exists(fn):
					result += [stage + "_" + l.asset_id]

			return result
		
		node = self.state.toc_loader.tree
		for p in parts:
			if p == "":
				continue
			if p not in node:
				node = None
				break
			node = node[p]

		if node is None:
			return []

		result = []
		for k in node:
			if isinstance(node[k], list):
				aid = node[k][0]
				locators = self.state.get_asset_variants_locators(stage, aid)
				for l in locators:
					fn = self._get_thumbnail_path(l)
					if os.path.exists(fn):
						result += [stage + "_" + aid]

		return result

	def _get_thumbnail(self, stage, aid):
		locators = self.state.get_asset_variants_locators(stage, aid)
		for l in locators:
			fn = self._get_thumbnail_path(l)
			if os.path.exists(fn):
				f = open(fn, "rb")
				return (flask.send_file(f, mimetype='image/png'), 200)

		return ("", 404)

	def _try_making_thumbnail(self, locator, data, asset):
		try:
			if data is None or asset is None:
				data, asset = self.state.get_asset(locator)

			if isinstance(asset, dat1lib.types.autogen.Texture):
				img = self.state.textures._load_dds_mipmap(asset, None, 0)
				if img is None:
					return False

				fn = self._get_thumbnail_path(locator) # don't calculate metahash unless this is a thumbnailable asset, such as texture

				if DEBUG_DDS:
					img.save(".cache/thumbnails/orig_{}.png".format(aid))

				w, h = img.size
				max_side = w
				if h > max_side:
					max_side = h
				scale = 64/max_side
				new_width = max(int(w * scale), 1)
				new_height = max(int(h * scale), 1)
				img = img.resize((new_width, new_height), Image.ANTIALIAS)
				img.save(fn)
				return True
		except:
			print(traceback.format_exc())

		return False
