import dat1lib
import dat1lib.crc64 as crc64
import io
import os.path
import re
import struct
import zipfile

def is_pathlike(s):
	return (s is not None and "." in s and ("/" in s or "\\" in s))

class StagesSuitImporter(object):
	def __init__(self, stages):
		self.stages = stages

	def import_suit(self, suit, stage):
		zf = zipfile.ZipFile(suit)
		stage_object, _ = self.stages.get_stage(stage)

		#

		id_fn = None
		files_dir = None
		for n in zf.namelist():
			if os.path.basename(n) == "id.txt":
				id_fn = n
				files_dir = os.path.dirname(n)
				break

		suitname = zf.read(id_fn).decode("ascii")
		info = zf.read(files_dir + "/info.txt")
		container = zf.read(files_dir + "/" + suitname)

		#

		SIZE = 21
		count = len(info) // SIZE
		entries = [struct.unpack("<IIIQB", info[i*SIZE:(i+1)*SIZE]) for i in range(count)]

		possible_paths = {}
		self.make_path(possible_paths, "ui\\textures\\pause\\character\\suit_{}.texture".format(suitname))
		self.make_path(possible_paths, "configs\\inventory\\inv_reward_loadout_{}.config".format(suitname))
		self.make_path(possible_paths, "configs\\equipment\\equip_techweb_suit_{}.config".format(suitname))
		self.make_path(possible_paths, "configs\\masteritemloadoutlist\\itemloadout_spiderman_{}.config".format(suitname))

		for e in entries:
			self.make_paths_from_asset(e, container, possible_paths)

		for e in entries:
			self.import_asset(stage_object, e, container, possible_paths)

		return {"success": True}

	#

	def make_path(self, paths, path):
		def normalize_path(path):
			return path.lower().replace('\\', '/') # TODO: utils

		path_normalized = normalize_path(path)
		aid = crc64.hash(path_normalized)
		paths["{:016X}".format(aid)] = path_normalized

	#

	def make_paths_from_asset(self, suit_info_entry, container, possible_paths):
		try:
			off, _, sz, aid, span_to_append_to = suit_info_entry
			asset_data = container[off:off+sz]
			asset = dat1lib.read(io.BytesIO(asset_data), try_unknown=False)

			self.make_paths_from_strings_block(asset, possible_paths)
			self.make_paths_from_vanity_config(asset, possible_paths)
			self.make_paths_from_model_materials(asset, possible_paths)
			self.make_paths_from_material_textures(asset, possible_paths)
		except:
			pass

	def make_paths_from_strings_block(self, asset, possible_paths):
		try:
			strings_map = asset.dat1._strings_map
			for k in strings_map:
				s = strings_map[k]
				if is_pathlike(s):
					self.make_path(possible_paths, s)
		except:
			pass

	def make_paths_from_vanity_config(self, asset, possible_paths):
		# VanityItemConfig -> .model path (not in references section)
		try:
			s = asset.dat1.get_section(0xE501186F).root["ModelList"]["Model"]["AssetPath"] # TODO: Config.get_section
			if is_pathlike(s):
				self.make_path(possible_paths, s)
		except:
			pass

	def make_paths_from_model_materials(self, asset, possible_paths):
		def read_string(data, index):
			start = index
			i = index
			
			while i < len(data):
				if data[i] == 0 or i == len(data)-1:
					if start == i:
						return ""

					return data[start:i].decode('ascii')

				i += 1

			return data[start:].decode('ascii')

		# .models with .material paths put outside of strings block
		try:
			materials_section = asset.dat1.get_section(0x3250BB80)
			for i, q in enumerate(materials_section.triples):
				offset = materials_section.string_offsets[i][0]
				s = read_string(asset._raw_dat1, offset) # q[0] should be crc64(s)
				if is_pathlike(s):
					self.make_path(possible_paths, s)
		except:
			pass

	def make_paths_from_material_textures(self, asset, possible_paths):
		try:
			serialized_data_section = asset.dat1.get_section(0xF5260180)

			for (pos, _) in serialized_data_section.textures:
				s = serialized_data_section._get_string(pos)
				if is_pathlike(s):
					self.make_path(possible_paths, s)
		except:
			pass

	#

	def import_asset(self, stage, suit_info_entry, container, possible_paths):
		off, _, sz, aid, span_to_append_to = suit_info_entry

		asset_path = self.make_asset_path("{:016X}".format(aid), possible_paths)
		asset_data = container[off:off+sz]
		stage.stage_asset_data(asset_path, span_to_append_to, asset_data)

	def make_asset_path(self, aid, possible_paths):
		path = aid
		if aid in possible_paths:
			path = possible_paths[aid]
		elif aid in self.stages.state.toc_loader._known_paths:
			path = self.stages.state.toc_loader._known_paths[aid]
		return path
