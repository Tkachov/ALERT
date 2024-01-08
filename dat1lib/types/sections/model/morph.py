import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

# based off of sleepyzay's https://github.com/sleepyzay/insomniac-model/blob/main/rac%20ra%20-%20blender.py

class MorphInfo(object):
	def __init__(self, data, offset):
		self.name_hash, self.name_offset, self.data_offset, self.indexes_offset = struct.unpack("<4I", data[offset:offset+16])
		self.packing_count, self.packing_bits, self.packing_bits2, self.packing_null = struct.unpack("<4B", data[offset+16:offset+20])
		self.position_scale, self.position_bias, self.normal_scale, self.normal_bias = struct.unpack("<4f", data[offset+20:offset+36])
		self.subset_count, self.subset_info_len, self.data_len, self.ndx_len = struct.unpack("<HHII", data[offset+36:offset+48])

		def unpack_N_units_at_offset(data, fmt, offset, N):
			sz = struct.calcsize(fmt)
			return ([struct.unpack(fmt, data[offset + i*sz:offset + (i+1)*sz])[0] for i in range(N)], sz*N)

		def align(value, d):
			rem = value % d
			aln = 0
			if rem > 0:
				aln = d - rem
			return value + aln

		cur_offset = offset+48
		self.subset_ids, read_bytes = unpack_N_units_at_offset(data, "<b", cur_offset, self.subset_count)
		cur_offset += read_bytes
		cur_offset = align(cur_offset, 4)

		self.subset_vertex_offsets, read_bytes = unpack_N_units_at_offset(data, "<I", cur_offset, self.subset_count)
		cur_offset += read_bytes

		self.subset_index_offsets, read_bytes = unpack_N_units_at_offset(data, "<I", cur_offset, self.subset_count)
		cur_offset += read_bytes

		self.subset_vertex_counts, read_bytes = unpack_N_units_at_offset(data, "<H", cur_offset, self.subset_count)
		cur_offset += read_bytes
		cur_offset = align(cur_offset, 4)

		self.subset_data_table_indexes, read_bytes = unpack_N_units_at_offset(data, "<H", cur_offset, self.subset_count)
		cur_offset += read_bytes
		cur_offset = align(cur_offset, 4)

		self.subset_data_tables = []
		for i in range(self.subset_count):
			tables = []
			total_vertexes = 0

			cur_offset2 = cur_offset + self.subset_data_table_indexes[i] * 6
			while total_vertexes < self.subset_vertex_counts[i]:
				table = struct.unpack("<HI", data[cur_offset2:cur_offset2+6]) # (vertexes_count, indexes_count)
				tables += [table]
				cur_offset2 += 6
				total_vertexes += table[0]

			self.subset_data_tables += [tables]

class ModelAnimMorphInfoSection(dat1lib.types.sections.Section):
	TAG = 0x380A5744 # Model Anim Morph Info
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 255 occurrences in 38298 files
		# size = 172..115360 (avg = 32789.6)
		#
		# examples: 8B2690F460D2A381 (min size), 9870FFAD9BAF955A (max size)

		# MM
		# 66 occurrences in 37147 files
		# size = 172..286160 (avg = 27620.9)
		#
		# examples: 91ECBF742BD80C48 (min size), 97A26AEB21F75DC8 (max size)

		# RCRA
		# 19 occurrences in 11387 files
		# size = 292..79112 (avg = 53322.9)
		#
		# examples: 8455ADEAEACE6204 (min size), 93E189C6F48429E9 (max size)

		self.unk1, self.buffers_len, self.count, self.mirror_count, self.info_table_offset, self.mirror_info_table_offset, self.unk2 = struct.unpack("<IIHHIII", data[:24])

		# buffers_len = len(ModelAnimMorphDataSection.data) + len(ModelAnimMorphIndicesSection.data)
		# also, these 3 sections seem to always to go one after another (0x380A5744/info, 0x5E709570/data, 0xA600C108/indices)

		def unpack_N_structs_at_offset(data, fmt, offset, N):
			sz = struct.calcsize(fmt)
			return [struct.unpack(fmt, data[offset + i*sz:offset + (i+1)*sz]) for i in range(N)]

		self.morph_tables = unpack_N_structs_at_offset(data, "<II", self.info_table_offset, self.count) # (name_hash, info_offset)
		self.morph_mirror_tables = unpack_N_structs_at_offset(data, "<II", self.mirror_info_table_offset, self.mirror_count) # (name_hash, name_hash2)
		self.morph_infos = [MorphInfo(data, offset) for _, offset in self.morph_tables]

	def get_short_suffix(self):
		return "Morph Info ({}, {})".format(self.count, self.mirror_count)

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Morph Info   | {:6} entries, {:6} mirror ids".format(self.TAG, self.count, self.mirror_count))

		print()
		print(f"           unk1   = {self.unk1}")
		print(f"           buflen = {self.buffers_len}")
		print(f"           count  = {self.count}")
		print(f"           mirror = {self.mirror_count}")
		print(f"           off1   = {self.info_table_offset}")
		print(f"           off2   = {self.mirror_info_table_offset}")
		print(f"           unk2   = {self.unk2}")

		print("")
		#######........ | 123  12345678  12345678  123 123 123 123
		#######                                    12345678  12345678
		print("           #    hash      name")
		print("                data_off  ndx_off   <-  packing  ->")
		print("                pos scale/bias      normal scale/bias")
		print("         ---------------------------------------------")
		for i, info in enumerate(self.morph_infos):
			print("         - {:<3}  {:08X}  {}".format(i, info.name_hash, self._dat1.get_string(info.name_offset)))
			print("                {:<8}  {:<8}  {:<3} {:<3} {:<3} {:3}".format(info.data_offset, info.indexes_offset, info.packing_count, info.packing_bits, info.packing_bits2, info.packing_null))
			print("                {:<8.3f}  {:<8.3f}  {:<8.3f} {:<8.3f}".format(info.position_scale, info.position_bias, info.normal_scale, info.normal_bias))
			print("                subsets: {}".format(info.subset_count))
			print("                    {}".format(info.subset_ids))
			print("                    {}".format(info.subset_vertex_offsets))
			print("                    {}".format(info.subset_index_offsets))
			print("                    {}".format(info.subset_vertex_counts))
			print("                    {}".format(info.subset_data_table_indexes))
			print("                    {}".format(info.subset_data_tables))
			print()

		print("")

		if self.mirror_count > 0:
			#######........ | 123  12345678  12345678
			print("           #         key     value")
			print("         -------------------------")
			for i, l in enumerate(self.morph_mirror_tables):
				print("         - {:<3}  {:08X}  {:08X}".format(i, l[0], l[1]))
		else:
			print("         No mirror ids.")

#

class ModelAnimMorphDataSection(dat1lib.types.sections.Section):
	TAG = 0x5E709570 # Model Anim Morph Data
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 255 occurrences in 38298 files
		# size = 1248..12720124 (avg = 1245716.2)
		#
		# examples: A296B03EFEBF937A (min size), A20532A6756AC4AE (max size)

		# MM
		# 66 occurrences in 37147 files
		# size = 480..7788288 (avg = 1321672.7)
		#
		# examples: BD8E0CB2CF2185EC (min size), 9DE5B2D46357DB69 (max size)

		# RCRA
		# 19 occurrences in 11387 files
		# size = 102192..12314252 (avg = 7375643.5)
		#
		# examples: 99F087989A2594FB (min size), B1C377CA094E4902 (max size)
		pass

	def save(self):
		of = io.BytesIO(bytes())
		of.write(self._raw)
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Morph Data ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return

		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Morph Data   | {:6} bytes".format(self.TAG, len(self._raw)))

	def web_repr(self):
		return {"name": "Model Anim Morph Data", "type": "text", "readonly": True, "content": "{} bytes".format(len(self._raw))}

#

class ModelAnimMorphIndicesSection(dat1lib.types.sections.Section):
	TAG = 0xA600C108 # Model Anim Morph Indices
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 255 occurrences in 38298 files
		# size = 76..709280 (avg = 133422.9)
		#
		# examples: A296B03EFEBF937A (min size), 9870FFAD9BAF955A (max size)

		# MM
		# 66 occurrences in 37147 files
		# size = 12..931032 (avg = 151739.9)
		#
		# examples: BD8E0CB2CF2185EC (min size), 9DE5B2D46357DB69 (max size)

		# RCRA
		# 19 occurrences in 11387 files
		# size = 2380..658056 (avg = 344779.1)
		#
		# examples: BF6DD7D3DE8A301B (min size), 96D2CE8B17C5471D (max size)
		pass

	def save(self):
		of = io.BytesIO(bytes())
		of.write(self._raw)
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Morph Indices ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return

		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Morph Indxes | {:6} bytes".format(self.TAG, len(self._raw)))

	def web_repr(self):
		return {"name": "Model Anim Morph Indices", "type": "text", "readonly": True, "content": "{} bytes".format(len(self._raw))}
