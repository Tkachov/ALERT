import base64
import dat1lib
import dat1lib.types.toc
import dat1lib.types.autogen
import dat1lib.types.sections.texture.autogen
import io
import os
import os.path
import platform
import server.obj_writer
import struct
import subprocess
import sys
import traceback
import zlib
from flask import send_file
from PIL import Image

DEBUG_DDS = False

class State(object):
	def __init__(self):
		self._reset()

	def _reset(self):
		self.toc = None
		self.toc_path = None

		self.currently_extracted_asset = None
		self.currently_extracted_asset_index = None
		self.currently_extracted_asset_data = None

		self.tree = None
		self.hashes = {}
		self._known_paths = {}
		self.archives = []

		self.edited_asset = None
		self.edited_asset_name = None

		self.has_texconv = False

	def _insert_path(self, path, aid):
		parts = path.split("/")
		dirs, file = parts[:-1], parts[-1]
		
		node = self.tree
		for d in dirs:
			if d not in node:
				node[d] = {}
			node = node[d]

		node[file] = [aid, []]
		self._known_paths[aid] = path

	def _add_index_to_tree(self, aid, i, archive_index):
		path = self._known_paths[aid]
		parts = path.split("/")
		dirs, file = parts[:-1], parts[-1]
		
		node = self.tree
		for d in dirs:
			if d not in node:
				node[d] = {}
			node = node[d]

		node[file][1] += [[i, archive_index]]

	def _load_tree(self):
		if self.tree is not None:
			return

		self.tree = {}

		def normalize_path(path):
			return path.lower().replace('\\', '/').strip()

		try:
			with open("hashes.txt", "r") as f:
				for line in f:
					try:
						parts = line.split(",")
						aid, path = parts[0], normalize_path(parts[1])
						if path != "":
							self._insert_path(path, aid)
					except:
						pass
		except:
			pass

	def load_toc(self, path):		
		self._load_tree()

		# TODO: toc is not None

		asset_archive_path = os.path.dirname(path)
		toc_fn = path

		if os.path.isdir(path):
			asset_archive_path = path
			toc_fn = os.path.join(path, "toc")

		if self.toc_path is not None:
			try:
				if os.path.samefile(self.toc_path, toc_fn):
					# don't do anything, it's already loaded
					# TODO: parameter to force reload?
					return
			except:
				# `samefile` not available on Windows
				pass

			# TODO: not the same, should we "unload" it (if error happens, we'd still be working with old one, which might be confusing for user -- as if new one loaded correctly)
			self._reset()
			self._load_tree()

		#

		toc = None
		with open(toc_fn, "rb") as f:
			toc = dat1lib.read(f)		

		if toc is None:
			raise Exception("Couldn't comprehend '{}'".format(toc_fn))

		if not isinstance(toc, dat1lib.types.toc.TOC):
			raise Exception("Not a toc")
	
		#

		toc.set_archives_dir(asset_archive_path)

		self.toc = toc
		self.toc_path = toc_fn

		assets_section = self.toc.get_assets_section()
		offsets_section = self.toc.get_offsets_section()
		ids = assets_section.ids
		for i in range(len(ids)):
			aid = "{:016X}".format(ids[i])
			if aid in self._known_paths:
				self._add_index_to_tree(aid, i, offsets_section.entries[i].archive_index)
			else:
				if aid in self.hashes:
					self.hashes[aid] += [[i, offsets_section.entries[i].archive_index]]
				else:
					self.hashes[aid] = [[i, offsets_section.entries[i].archive_index]] # ["", [i]]

		archives_section = self.toc.get_archives_section()
		self.archives = ["{}".format(a.filename.decode('ascii')).replace("\x00", "") for a in archives_section.archives]

		#
		
		os.makedirs(".cache/thumbnails/", exist_ok=True)
		if platform.system() == "Windows" and os.path.exists("texconv.exe"):
			self.has_texconv = True

	def _read_asset(self, index):
		data = None

		try:
			data = self.toc.extract_asset(self.toc.get_asset_entry_by_index(index))
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
		s = self.toc.get_assets_section()
		aid = "{:016X}".format(s.ids[index])
		if aid in self._known_paths:
			return os.path.basename(self._known_paths[aid])
		return aid

	def _get_asset_metahash(self, index):
		assets_section = self.toc.get_assets_section()
		archives_section = self.toc.get_archives_section()
		offsets_section = self.toc.get_offsets_section()
		sizes_section = self.toc.get_sizes_section()
		archive_index = offsets_section.entries[index].archive_index
		checksum = zlib.crc32(archives_section.archives[archive_index].filename, 0)
		checksum = zlib.crc32(struct.pack("<QII", assets_section.ids[index], offsets_section.entries[index].offset, sizes_section.entries[index].value), checksum)
		return checksum

	def _get_thumbnail_path(self, aid, index):
		return ".cache/thumbnails/{}.{:08X}.png".format(aid, self._get_asset_metahash(index))

	def extract_asset(self, index):
		# TODO: what if I want to force reload?
		s = self.toc.get_sizes_section()
		sz = s.entries[index].value

		if self.currently_extracted_asset_index == index:
			return self.currently_extracted_asset, sz, None

		data, obj = self._read_asset(index)
		self.currently_extracted_asset = obj
		self.currently_extracted_asset_index = index
		self.currently_extracted_asset_data = data

		s = self.toc.get_assets_section()
		aid = "{:016X}".format(s.ids[index])
		made_thumbnail = self._try_making_thumbnail(aid, index)
		thumbnail = aid if made_thumbnail else None

		return self.currently_extracted_asset, sz, thumbnail

	def get_model(self, index):
		data, asset = self._get_asset_by_index(index)
		return server.obj_writer.write(asset)

	def get_asset_data(self, index):
		data, asset = self._get_asset_by_index(index)
		return data, self._get_asset_name(index)

	def get_asset_section_data(self, index, section):
		data, asset = self._get_asset_by_index(index)
		return asset.dat1.get_section(section)._raw, self._get_asset_name(index) + ".{:08X}.raw".format(section)

	def get_asset_strings(self, index):
		data, asset = self._get_asset_by_index(index)
		return asset.dat1._raw_strings_data, self._get_asset_name(index) + ".strings.raw"

	def get_asset_report(self, index):
		data, asset = self._get_asset_by_index(index)

		report = {"header": [], "sections": {}, "strings": ""}
		report["header"] = [(s.tag, s.offset, s.size) for s in asset.dat1.header.sections]

		#
		
		CONFIG = {
			"sections": True,
			"sections_verbose": True,
			"web": True
		}

		for ndx, s in enumerate(asset.dat1.header.sections):
			section = asset.dat1.sections[ndx]
			report["sections"][s.tag] = ""
			try:
				if section is not None:
					if "web_repr" in dir(section):
						report["sections"][s.tag] = section.web_repr()
					else:
						captured = io.StringIO()
						sys.stdout = captured
						section.print_verbose(CONFIG)
						report["sections"][s.tag] = {"name": "{:08X}".format(s.tag), "type": "text", "readonly": True, "content": captured.getvalue()}
						sys.stdout = sys.__stdout__

						try:
							if report["sections"][s.tag]["content"] == "": # TODO: make it part of web_repr()
								report["sections"][s.tag]["type"] = "bytes"
								report["sections"][s.tag]["offset"] = 0 # TODO: make it absolute, not section-relative
								report["sections"][s.tag]["content"] = base64.b64encode(section._raw).decode('ascii')
						except:
							pass
			except:
			 	pass

		#

		try:
			items = asset.dat1._strings_map.items()
			items = sorted(items, key=lambda x: x[0])
			########## 123  123456  ...
			result =  "#    offset  value\n"
			result += "------------------\n"
			for i, (offset, s) in enumerate(items):
				result += "{:<3}  {:6}  {}\n".format(i, offset, repr(s))
			report["strings"] = result
		except:
			pass

		#

		return report

	def get_asset_editor(self, index):
		data, asset = self._get_asset_by_index(index)

		#

		report = {
			"header": {"magic": 0, "size": 0, "rest": []},
			"strings": {"count": 0, "size": 0},
			"sections": [],
			"total_size": len(data)
		}

		#

		report["header"]["magic"], report["header"]["size"] = struct.unpack("<II", data[:8])
		report["header"]["rest"] = [struct.unpack("<I", data[8+i*4:12+i*4])[0] for i in range(7)]

		report["strings"]["count"] = len(asset.dat1._strings_map)
		report["strings"]["size"] = len(asset.dat1._raw_strings_data)

		#

		sorted_sections = [(s.tag, s.offset, s.size) for s in asset.dat1.header.sections]
		sorted_sections = sorted(sorted_sections, key=lambda x: x[1])

		for tag, _, size in sorted_sections:
			# TODO: web_editor_data()
			report["sections"] += [{"tag": tag, "size": size, "type": "raw"}]

		#

		return report

	def edit_asset(self, asset_index, header, strings, sections):
		_, asset = self._read_asset(asset_index) # a new copy instead of reusing existing one, because we're editing it
		dat1 = asset.dat1

		if strings["option"] == "replace":
			dat1._raw_strings_data = strings["raw"]
		
		elif strings["option"] == "append":
			lines = strings["appended"].replace('\r\n', '\n').replace('\r', '\n').split('\n')
			for l in lines:
				dat1.add_string(l)

		#

		index = 0
		for s in sections:
			tag = s["tag"]
			option = s["option"]

			for hs in dat1.header.sections:
				if hs.tag == tag:
					hs.offset = index
					break
			index += 1

			if option == "replace":
				dat1._sections_data[dat1._sections_map[tag]] = s["raw"]

		dat1.recalculate_section_headers()		

		#

		f = io.BytesIO(bytes())

		magic, size = int(header["magic"]), int(header["size"])
		if header["recalculate_size"]:
			size = dat1.header.size
		f.write(struct.pack("<II", magic, size))

		rest = header["rest"]
		for x in rest:
			f.write(struct.pack("<I", int(x)))

		dat1.save(f)
		f.seek(0)

		self.edited_asset = f
		self.edited_asset_name = self._get_asset_name(asset_index)

	def get_thumbnails_list(self, path):
		parts = path.split("/")
		
		node = self.tree
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
		s = self.toc.get_assets_section()
		for k in node:
			if isinstance(node[k], list):
				aid, variants = node[k][0], node[k][1]
				for index, archive_index in variants:
					aid = "{:016X}".format(s.ids[index])
					fn = self._get_thumbnail_path(aid, index)
					if os.path.exists(fn):
						result += [aid]

		return result

	def _get_node_by_aid(self, aid):
		path = self._known_paths[aid]
		parts = path.split("/")
		dirs, file = parts[:-1], parts[-1]
		
		node = self.tree
		for d in dirs:
			if d not in node:
				node[d] = {}
			node = node[d]

		return node[file]

	def get_thumbnail(self, aid):
		node = self._get_node_by_aid(aid)
		aid, variants = node[0], node[1]
		for index, archive_index in variants:
			fn = self._get_thumbnail_path(aid, index)
			if os.path.exists(fn):
				f = open(fn, "rb")
				return (send_file(f, mimetype='image/png'), 200)

		return ("", 404)

	def make_thumbnail(self, aid):
		node = self._get_node_by_aid(aid)
		aid, variants = node[0], node[1]

		for index, archive_index in variants:
			if self._try_making_thumbnail(aid, index):
				return True

		return False

	def _try_making_thumbnail(self, aid, index):
		try:
			fn = self._get_thumbnail_path(aid, index)
			data, asset = self._get_asset_by_index(index)

			if isinstance(asset, dat1lib.types.autogen.Texture):
				img = self._load_dds_mipmap(asset, None, 0)
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

	def _load_dds_mipmap(self, texture_asset, hd_data, mipmap_index):
		try:
			if isinstance(texture_asset, dat1lib.types.autogen.Texture):
				info = texture_asset.dat1.get_section(dat1lib.types.sections.texture.autogen.TextureHeaderSection.TAG)

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

	def get_texture_viewer(self, index):
		data, asset = self._get_asset_by_index(index)
		info = asset.dat1.get_section(dat1lib.types.sections.texture.autogen.TextureHeaderSection.TAG)

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

	def get_texture_mipmap(self, index, mipmap_index):
		data, asset = self._get_asset_by_index(index)
		info = asset.dat1.get_section(dat1lib.types.sections.texture.autogen.TextureHeaderSection.TAG)

		hd_data = None
		if mipmap_index < info.hd_mipmaps:
			s = self.toc.get_assets_section()
			aid = "{:016X}".format(s.ids[index])
			path = self._known_paths[aid]
			parts = path.split("/")
			dirs, file = parts[:-1], parts[-1]
			
			node = self.tree
			for d in dirs:
				if d not in node:
					node[d] = {}
				node = node[d]
			
			variants = node[file][1]
			if len(variants) == 2:
				hd_index = variants[0][0]
				if hd_index == index:
					hd_index = variants[1][0]		
			
			hd_data, ha = self._read_asset(hd_index)
		else:
			mipmap_index -= info.hd_mipmaps

		img = self._load_dds_mipmap(asset, hd_data, mipmap_index)
		f = io.BytesIO()
		img.save(f, format="png")
		f.seek(0)
		return (send_file(f, mimetype='image/png'), 200)
