import flask
from server.api_utils import get_field, make_get_json_route, make_post_json_route

import dat1lib.types.autogen
import dat1lib.types.sections.texture.autogen
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
		path = get_field(flask.request.form, "path")
		return {"list": self.get_thumbnails_list(path)}

	def get_png(self):
		aid = get_field(flask.request.args, "aid")
		return self._get_thumbnail(aid)

	# internal

	def boot(self):
		os.makedirs(".cache/thumbnails/", exist_ok=True)

	def _get_asset_metahash(self, index):
		toc = self.state.toc_loader.toc
		assets_section = toc.get_assets_section()
		archives_section = toc.get_archives_section()
		offsets_section = toc.get_offsets_section()
		sizes_section = toc.get_sizes_section()
		archive_index = offsets_section.entries[index].archive_index
		checksum = zlib.crc32(archives_section.archives[archive_index].filename, 0)
		checksum = zlib.crc32(struct.pack("<QII", assets_section.ids[index], offsets_section.entries[index].offset, sizes_section.entries[index].value), checksum)
		return checksum

	def _get_thumbnail_path(self, aid, index):
		return ".cache/thumbnails/{}.{:08X}.png".format(aid, self._get_asset_metahash(index))

	def get_thumbnails_list(self, path):
		parts = path.split("/")
		
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
		s = self.state.toc_loader.toc.get_assets_section()
		for k in node:
			if isinstance(node[k], list):
				aid, variants = node[k][0], node[k][1]
				for index, archive_index in variants:
					aid = "{:016X}".format(s.ids[index])
					fn = self._get_thumbnail_path(aid, index)
					if os.path.exists(fn):
						result += [aid]

		return result

	def _get_thumbnail(self, aid):
		node = self.state.toc_loader._get_node_by_aid(aid)
		aid, variants = node[0], node[1]
		for index, archive_index in variants:
			fn = self._get_thumbnail_path(aid, index)
			if os.path.exists(fn):
				f = open(fn, "rb")
				return (flask.send_file(f, mimetype='image/png'), 200)

		return ("", 404)

	def make_thumbnail(self, aid):
		node = self.state.toc_loader._get_node_by_aid(aid)
		aid, variants = node[0], node[1]

		for index, archive_index in variants:
			if self._try_making_thumbnail(aid, index):
				return True

		return False

	def _try_making_thumbnail(self, aid, index):
		try:
			fn = self._get_thumbnail_path(aid, index)
			data, asset = self.state._get_asset_by_index(index)

			if isinstance(asset, dat1lib.types.autogen.Texture):
				img = self.state.textures._load_dds_mipmap(asset, None, 0)
				if img is None:
					return False

				if DEBUG_DDS:
					img.save(".cache/thumbnails/orig_{}.png".format(aid))

				w, h = img.size
				max_side = w
				if h > max_side:
					max_side = h
				scale = 64/max_side
				new_width = int(w * scale)
				new_height = int(h * scale)
				img = img.resize((new_width, new_height), Image.ANTIALIAS)
				img.save(fn)
				return True
		except:
			print(traceback.format_exc())

		return False
