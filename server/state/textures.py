import flask
from server.api_utils import get_int, get_field, make_get_json_route, make_post_json_route

import dat1lib.types.autogen
import dat1lib.types.sections.texture.header
import io
import os
import os.path
import platform
import struct
import subprocess
import traceback
from PIL import Image

DEBUG_DDS = False

class Textures(object):
	def __init__(self, state):
		self.state = state
		self.has_texconv = False

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/textures_viewer/make", self.make_viewer)
		make_get_json_route(app, "/api/textures_viewer/mipmap", self.get_mipmap, False)

	def make_viewer(self):
		locator = get_field(flask.request.form, "locator")
		return {"viewer": self.get_texture_viewer(locator)}

	def get_mipmap(self):
		rq = flask.request
		locator = get_field(rq.args, "locator")
		mmi = get_int(rq.args, "mipmap_index")
		return self.get_texture_mipmap(locator, mmi)

	# internal

	def boot(self):
		if platform.system() == "Windows" and os.path.exists("texconv.exe"):
			self.has_texconv = True

	def _load_dds_mipmap(self, texture_asset, hd_data, mipmap_index):
		try:
			if isinstance(texture_asset, dat1lib.types.autogen.Texture):
				info = texture_asset.dat1.get_section(dat1lib.types.sections.texture.header.TextureHeaderSection.TAG)

				if DEBUG_DDS:
					print("{}x{}, fmt={}".format(info.sd_width, info.sd_height, info.fmt))

				mipmaps = []
				hd_bpp = 0
				if hd_data is not None:
					w, h = info.hd_width, info.hd_height
					for i in range(info.hd_mipmaps):
						hd_bpp += w*h
						mipmaps += [(w, h)]
						w = w // 2
						h = h // 2

				sd_bpp = 0				
				w, h = info.sd_width, info.sd_height
				for i in range(info.sd_mipmaps):
					sd_bpp += w*h
					mipmaps += [(w, h)]
					w = w // 2
					h = h // 2

				if hd_bpp > 0:
					hd_bpp = info.hd_len / hd_bpp
				if sd_bpp > 0:
					sd_bpp = info.sd_len / sd_bpp

				w, h = mipmaps[mipmap_index]

				dds_data = b"\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x0A\x00"
				dds_data += struct.pack("<II", h, w)

				# pitch / depth / mipmaps
				# pitch value is "unreliable", as specified in https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide, so I'm computing it badly
				pitch = (w * 32 + 7) // 8
				dds_data += struct.pack("<III", pitch, 0, 0)

				# reserved: 11 uint32s
				dds_data += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

				# pixelformat: size / flags / fourcc / bitcount / rgba masks / dwcaps[4] / reserved
				"""
				DDSCAPS_COMPLEX = 0x8
				DDSCAPS_TEXTURE = 0x1000
				DDSCAPS_MIPMAP = 0x400000
				"""
				DWCAPS0 = b"\x00\x10\x00\x00" # b"\x08\x10\x40\x00"
				dds_data += b"\x20\x00\x00\x00\x04\x00\x00\x00\x44\x58\x31\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
				dds_data += DWCAPS0
				dds_data += b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

				# dxt10: format / dimension / misc / arraysize / misc flags
				dds_data += struct.pack("<5I", info.fmt, 3 if h > 1 else 2, 0, 1, 0)

				pixels_written = False
				hd_mipmaps_count = 0
				if hd_data is not None:
					hd_mipmaps_count = info.hd_mipmaps
					if mipmap_index < info.hd_mipmaps:
						offset = 0
						for i in range(mipmap_index):
							mw, mh = mipmaps[i]
							offset += int(hd_bpp * mw * mh)
						dds_data += hd_data[offset:]
						pixels_written = True
					else:
						mipmap_index -= info.hd_mipmaps

				if not pixels_written:
					offset = 0x80 - 36
					for i in range(mipmap_index):
						mw, mh = mipmaps[i + hd_mipmaps_count]
						offset += int(sd_bpp * mw * mh)
					dds_data += texture_asset._raw_dat1[offset:]
				
				if self.has_texconv:
					def _remove_file(fn):
						try:
							os.remove(fn)
						except:
							pass

					try:
						f = open(".cache/mipmap.dds", "wb")
						f.write(dds_data)
						f.close()

						p = subprocess.Popen("texconv.exe mipmap.dds -ft png -y", cwd='.cache')
						try:
							p.wait(15)
						except:
							try:
								p.kill()
							except:
								pass
							return None

						image = Image.open(".cache/mipmap.png")

						_remove_file(".cache/mipmap.dds")
						_remove_file(".cache/mipmap.png")

						return image
					except:					
						print(traceback.format_exc())

				return Image.open(io.BytesIO(dds_data))
		except:
			print(traceback.format_exc())
			
		return None

	def get_texture_viewer(self, locator):
		data, asset = self.state._get_asset_by_locator(locator)
		info = asset.dat1.get_section(dat1lib.types.sections.texture.header.TextureHeaderSection.TAG)

		mipmaps = []

		w, h = info.hd_width, info.hd_height
		for i in range(info.hd_mipmaps):
			mipmaps += [(w, h)]
			w = w // 2
			h = h // 2

		w, h = info.sd_width, info.sd_height
		for i in range(info.sd_mipmaps):
			mipmaps += [(w, h)]
			w = w // 2
			h = h // 2

		return {"mipmaps": mipmaps}

	def get_texture_mipmap(self, locator, mipmap_index):
		data, asset = self.state._get_asset_by_locator(locator)
		info = asset.dat1.get_section(dat1lib.types.sections.texture.header.TextureHeaderSection.TAG)

		hd_data = None
		if mipmap_index < info.hd_mipmaps:
			hd_locator = self.state._make_hd_locator(locator)
			hd_data, ha = self.state.get_asset(hd_locator)
		else:
			mipmap_index -= info.hd_mipmaps

		img = self._load_dds_mipmap(asset, hd_data, mipmap_index)
		f = io.BytesIO()
		img.save(f, format="png")
		f.seek(0)
		return (flask.send_file(f, mimetype='image/png'), 200)
