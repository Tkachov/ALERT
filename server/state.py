import dat1lib
import dat1lib.types.toc
import io
import obj_writer
import os.path
import sys
import StringIO
import struct

class State(object):	
	def __init__(self):
		self.toc = None
		self.toc_path = None

		self.currently_extracted_asset = None
		self.currently_extracted_asset_index = None
		self.currently_extracted_asset_data = None

		self.tree = None
		self.hashes = {}
		self._known_paths = {}
		self.archives = []

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

		asset_archive_path = os.path.basename(path)
		toc_fn = path

		if os.path.isdir(path):
			asset_archive_path = path
			toc_fn = os.path.join(path, "toc")

		if self.toc_path is not None:
			if os.path.samefile(self.toc_path, toc_fn):
				# don't do anything, it's already loaded
				# TODO: parameter to force reload?
				return

			# TODO: not the same, should we "unload" it (if error happens, we'd still be working with old one, which might be confusing for user -- as if new one loaded correctly)

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

		s = self.toc.get_assets_section()
		s2 = self.toc.get_offsets_section()
		ids = s.ids
		for i in xrange(len(ids)):
			aid = "{:016X}".format(ids[i])
			if aid in self._known_paths:
				self._add_index_to_tree(aid, i, s2.entries[i].archive_index)
			else:
				if aid in self.hashes:
					self.hashes[aid] += [[i, s2.entries[i].archive_index]]
				else:
					self.hashes[aid] = [[i, s2.entries[i].archive_index]] # ["", [i]]

		s3 = self.toc.get_archives_section()
		self.archives = ["{}".format(a.filename) for a in s3.archives]

	def _read_asset(self, index):
		data = None

		try:
			data = self.toc.extract_asset(self.toc.get_asset_entry_by_index(index))
		except Exception as e:
			error_msg = "{}".format(e)

			if "Errno 2" in error_msg and "No such file or directory" in error_msg:
				def rindex(lst, value):
					return len(lst) - lst[::-1].index(value) - 1

				ri1 = rindex(error_msg, '/')
				ri2 = rindex(error_msg, '\\')
				if ri1 < ri2:
					ri1 = ri2

				raise Exception("missing archive '{}".format(error_msg[ri1+1:]))

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

	def extract_asset(self, index):
		# TODO: what if I want to force reload?
		s = self.toc.get_sizes_section()
		sz = s.entries[index].value

		if self.currently_extracted_asset_index == index:
			return self.currently_extracted_asset, sz

		data, obj = self._read_asset(index)
		self.currently_extracted_asset = obj
		self.currently_extracted_asset_index = index
		self.currently_extracted_asset_data = data

		return self.currently_extracted_asset, sz

	def get_model(self, index):
		data, asset = self._get_asset_by_index(index)
		return obj_writer.write(asset)

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
						captured = StringIO.StringIO()
						sys.stdout = captured
						section.print_verbose(CONFIG)
						report["sections"][s.tag] = {"name": "{:08X}".format(s.tag), "type": "text", "readonly": True, "content": captured.getvalue()}
						sys.stdout = sys.__stdout__
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
				result += "{:<3}  {:6}  {}\n".format(i, offset, s)
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
		report["header"]["rest"] = [struct.unpack("<I", data[8+i*4:12+i*4])[0] for i in xrange(7)]

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
