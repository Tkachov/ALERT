import flask
from server.api_utils import get_field, make_post_json_route

import dat1lib
import dat1lib.types.toc
import dat1lib.types.toc2
import dat1lib.types.autogen
import io
import os
import os.path
import platform

class TocLoader(object):
	def __init__(self, state):
		self.state = state
		self.reboot()

	def reboot(self):
		self.toc = None
		self.toc_path = None

		self.tree = None
		self.hashes = {}
		self._known_paths = {}
		self.archives = []

	# API

	def make_api_routes(self, app):
		pass

	# internal

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

	def _add_index_to_tree(self, aid, asset_info):
		path = self._known_paths[aid]
		parts = path.split("/")
		dirs, file = parts[:-1], parts[-1]
		
		node = self.tree
		for d in dirs:
			if d not in node:
				node[d] = {}
			node = node[d]

		node[file][1] += [asset_info]

	def _load_tree(self):
		if self.tree is not None:
			return

		self.tree = {}

		def normalize_path(path):
			return path.lower().replace('\\', '/').strip()

		try:
			if dat1lib.VERSION_OVERRIDE == dat1lib.VERSION_SO:
				with open("hashes_so.txt", "r") as f:
					for line in f:
						try:
							parts = line[:-1].split("\t")
							aid, path = parts[0], normalize_path(parts[1])
							if path != "":
								self._insert_path(path, "00000000" + aid)
						except:
							pass
			else:
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
			if os.path.samefile(self.toc_path, toc_fn):
				# don't do anything, it's already loaded
				# TODO: parameter to force reload?
				return

			# TODO: not the same, should we "unload" it (if error happens, we'd still be working with old one, which might be confusing for user -- as if new one loaded correctly)
			self.state.reboot()
			self._load_tree()

		#

		toc = None
		with open(toc_fn, "rb") as f:
			toc = dat1lib.read(f)

		if toc is None:
			raise Exception("Couldn't comprehend '{}'".format(toc_fn))

		if not isinstance(toc, dat1lib.types.toc.TOC) and not isinstance(toc, dat1lib.types.toc2.TOC2):
			raise Exception("Not a toc")
	
		#

		toc.set_archives_dir(asset_archive_path)

		self.toc = toc
		self.toc_path = toc_fn

		spans_section = self.toc.get_spans_section()
		assets_section = self.toc.get_assets_section()
		offsets_section = self.toc.get_offsets_section()
		sizes_section = self.toc.get_sizes_section()

		spans = spans_section.entries
		ids = assets_section.ids
		sizes = sizes_section.entries

		if toc.version == dat1lib.VERSION_RCRA or sizes_section.version == dat1lib.VERSION_RCRA:
			for span_index, span in enumerate(spans):
				for i in range(span.asset_index, span.asset_index + span.count):
					aid = "{:016X}".format(ids[i])
					asset_info = [span_index, sizes[i].archive_index, sizes[i].value]
					if aid in self._known_paths:
						self._add_index_to_tree(aid, asset_info)
					else:
						if aid in self.hashes:
							self.hashes[aid] += [asset_info]
						else:
							self.hashes[aid] = [asset_info]
		else:
			offsets = offsets_section.entries

			for span_index, span in enumerate(spans):
				for i in range(span.asset_index, span.asset_index + span.count):
					aid = "{:016X}".format(ids[i])
					asset_info = [span_index, offsets[i].archive_index, sizes[i].value]
					if aid in self._known_paths:
						self._add_index_to_tree(aid, asset_info)
					else:
						if aid in self.hashes:
							self.hashes[aid] += [asset_info]
						else:
							self.hashes[aid] = [asset_info]

		def cleanup_tree(node):
			keys_to_remove = []

			for k in node:
				if isinstance(node[k], list):
					aid, variants = node[k]
					if len(variants) == 0:
						keys_to_remove += [k]
				else:
					cleanup_tree(node[k])
					if len(node[k]) == 0:
						keys_to_remove += [k]

			for k in keys_to_remove:
				del node[k]

		cleanup_tree(self.tree)

		#

		def cleanup_tree(node):
			keys_to_remove = []

			for k in node:
				if isinstance(node[k], list):
					aid, variants = node[k]
					if len(variants) == 0:
						keys_to_remove += [k]
				else:
					cleanup_tree(node[k])
					if len(node[k]) == 0:
						keys_to_remove += [k]

			for k in keys_to_remove:
				del node[k]

		cleanup_tree(self.tree)

		#

		def get_archive_name(a):
			# "{}".format(a.filename.decode('ascii')).replace("\x00", "")
			archive_fn = a.filename
			zero = 0
			for zero in range(len(archive_fn)):
				if archive_fn[zero] == 0:
					break
			archive_fn = archive_fn[:zero]
			return "{}".format(archive_fn.decode('ascii')).replace("\x00", "")

		archives_section = self.toc.get_archives_section()
		self.archives = [get_archive_name(a) for a in archives_section.archives]

	def _get_node_by_aid(self, aid):
		if aid not in self._known_paths:
			return aid, self.hashes[aid]
		
		path = self._known_paths[aid]
		parts = path.split("/")
		dirs, file = parts[:-1], parts[-1]
		
		node = self.tree
		for d in dirs:
			if d not in node:
				node[d] = {}
			node = node[d]

		return node[file]

	#

	def get_boot_info(self):
		archives = self.toc.get_archives_section()
		assets = self.toc.get_assets_section()

		return {"toc": {
			"archives": len(archives.archives),
			"assets": len(assets.ids),
			"tree": self.tree,
			"assets_map": self.hashes,
			"archives_map": self.archives
		}}
