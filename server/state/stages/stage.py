import dat1lib.crc64 as crc64
import os
import os.path
import re

def normalize_path(path):
	return path.lower().replace('\\', '/').strip()

class Stage(object):
	def __init__(self, path):
		self.path = path
		self.reload()

	def reload(self):
		self.tree = {}
		self.aid_to_path = {}
		self.spans = []

		for fn in os.listdir(self.path):
			full_fn = os.path.join(self.path, fn)
			if os.path.isdir(full_fn):
				self.add_span(fn, full_fn)

	#

	def add_span(self, span_name, path):
		self.spans += [span_name]

		dirs = [""]
		while len(dirs) > 0:
			current_dir = dirs[0]
			dirs = dirs[1:]

			full_dir = os.path.join(path, current_dir)
			for fn in os.listdir(full_dir):
				full_fn = os.path.join(full_dir, fn)
				aid_fn = os.path.join(current_dir, fn)
				if os.path.isdir(full_fn):
					dirs += [aid_fn]
				else:
					if current_dir == "" and len(fn) == 16 and re.match("^[A-Fa-f0-9]{16}$", fn):
						aid_fn = fn.upper() # TODO: reassess; this makes it uppercase to be displayed in UI, but on a case-sensitive FS we won't find this file if it happens to be not in uppercase
						aid = aid_fn
					else:
						aid_fn = normalize_path(aid_fn)
						aid = "{:016X}".format(crc64.hash(aid_fn))
					self._insert_path(aid_fn, aid)
					asset_info = [span_name, 0, os.path.getsize(full_fn)]
					self._add_index_to_tree(aid, asset_info)

	def _insert_path(self, path, aid):
		if aid in self.aid_to_path:
			return

		self.aid_to_path[aid] = path

		parts = path.split("/")
		dirs, file = parts[:-1], parts[-1]
		
		node = self.tree
		for d in dirs:
			if d not in node:
				node[d] = {}
			node = node[d]

		node[file] = [aid, []]

	def _add_index_to_tree(self, aid, asset_info):
		path = self.aid_to_path[aid]
		parts = path.split("/")
		dirs, file = parts[:-1], parts[-1]
		
		node = self.tree
		for d in dirs:
			if d not in node:
				node[d] = {}
			node = node[d]

		node[file][1] += [asset_info]

	#

	def stage_asset_from_toc(self, path, locator, state):
		asset_data = state.get_asset_data(locator)
		self.stage_asset_data(path, locator.span, asset_data)

	def stage_asset_from_stage(self, path, locator, state):
		asset_data = state.get_asset_data(locator)
		span_index = int(locator.span) # TODO
		self.stage_asset_data(path, span_index, asset_data)

	def stage_asset_data(self, path, span_index, data):
		# TODO: maintain correct structs state
		real_path = os.path.join(self.path, self._get_span(span_index), path)

		dir_path = os.path.dirname(real_path)
		os.makedirs(dir_path, exist_ok=True)

		f = open(real_path, "wb")
		f.write(data)
		f.close()

	def _get_span(self, span_index):
		# TODO: span mappings
		return "{}".format(span_index)

	#

	def get_asset_variants_locators(self, stage_name, aid):
		path = self.aid_to_path[aid]
		results = []
		for s in self.spans:
			full_fn = os.path.join(self.path, s, path)
			if os.path.isfile(full_fn):
				results += ["{}/{}/{}".format(stage_name, s, path)]
		return results

	def get_assets_under_path(self, state, stage_name, path):
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
		for k in node:
			if isinstance(node[k], list):
				aid = node[k][0]
				result += state.get_asset_variants_locators(stage_name, aid)
		return result
