import dat1lib.types.sections
import io
import struct

class MeshDefinition(object):
	def __init__(self, data):
		self.unknowns = struct.unpack("<IQHHHH", data[:20])
		# ?, mesh_id, ?, ?, ?, ?
		self.vertexStart, self.indexStart, self.indexCount, self.vertexCount = struct.unpack("<IIII", data[20:36])
		self.flags, self.material_index, self.first_skin_batch, self.skin_batches_count = struct.unpack("<HHHH", data[36:44])
		self.unknowns2 = struct.unpack("<HHff", data[44:56]) # ?, ? | ?, ?
		self.first_weight_index, self.unknown3 = struct.unpack("<II", data[56:]) # first weight index in CCBAFF15 (at least in RCRA) -- basically equal to vertexStart, ?

	def get_id(self):
		return self.unknowns[1]

	def get_flags(self):
		return self.flags # 0x10 -- indexes are relative to mesh or not (maybe also means they are delta-encoded?)

	def get_material(self):
		return self.material_index

class MeshesSection(dat1lib.types.sections.Section):
	TAG = 0x78D9CBDE # Model Subset
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 38298 occurrences in 38298 files (always present)
		# size = 64..56064 (avg = 305.0)
		#
		# examples: 800058C35E144B3F (min size), 857E2B6AE905140D (max size)

		# MM
		# 37144 occurrences in 37147 files
		# size = 64..66944 (avg = 296.8)
		#
		# examples: 800058C35E144B3F (min size), 8C7796FC7478109D (max size)

		# RCRA
		# 11363 occurrences in 11387 files
		# size = 64..111744 (avg = 600.3)
		#
		# examples: 800653F4B380A1B1 (min size), 90A86BB170C341AA (max size)

		ENTRY_SIZE = 64
		count = len(data)//ENTRY_SIZE
		self.meshes = [MeshDefinition(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for m in self.meshes:
			of.write(struct.pack("<IQHHHH", *m.unknowns))
			of.write(struct.pack("<IIII", m.vertexStart, m.indexStart, m.indexCount, m.vertexCount))
			of.write(struct.pack("<HHHH", m.flags, m.material_index, m.first_skin_batch, m.skin_batches_count))
			of.write(struct.pack("<HHff", *m.unknowns2))
			of.write(struct.pack("<II", m.first_weight_index, m.unknown3))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "meshes ({})".format(len(self.meshes))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Mesh Defs    | {:6} meshes".format(self.TAG, len(self.meshes)))

		materials_section = self._dat1.get_section(0x3250BB80)

		print("")
		#######........ | 123  1234567812345678  12345678  12345678  12345678  12345678  12345678
		print("           #             mesh_id  vert_off  vertexes  indx_off   indexes  material")
		print("                               ?         ?         ?         ?         ?")
		print("                           flags  sknb_off  sknb_cnt         ?         ?")
		print("                                         ?         ?  rcra_wgt         ?")
		print("         -------------------------------------------------------------------------")

		for i, l in enumerate(self.meshes):
			u1, mid, u2, u3, u4, u5 = l.unknowns
			u9, u10, u11, u12 = l.unknowns2

			mat = l.material_index
			material_formatted = "#{}".format(mat)
			try:
				matname = self._dat1.get_string(materials_section.string_offsets[mat][1])
				if matname is not None:
					material_formatted = matname
			except:
				pass

			print("         - {:<3}  {:016X}  {:8}  {:8}  {:8}  {:8}  {}".format(i, mid, l.vertexStart, l.vertexCount, l.indexStart, l.indexCount, material_formatted))
			prefix = " "*8
			print("                {}{:08X}  {:8}  {:8}  {:8}  {:8}".format(prefix, u1, u2, u3, u4, u5))
			print("                {}{:8X}  {:8}  {:8}  {:8}  {:8}".format(prefix, l.flags, l.first_skin_batch, l.skin_batches_count, u9, u10))
			print("                {}          {:8.3}  {:8.3}  {:8}  {:8}".format(prefix, u11, u12, l.first_weight_index, l.unknown3))
			print("")
