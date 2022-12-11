import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class MaterialSerializedDataSection(dat1lib.types.sections.Section):
	TAG = 0xF5260180 # Material Serialized Data
	TYPE = 'material'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 13170 occurrences in 13178 files
		# size = 48..3552 (avg = 450.7)
		#
		# examples: 8010653ABB4F13F1 (min size), 8D5EB677647A4385 (max size)

		# MM
		# 11763 occurrences in 11787 files
		# size = 48..2640 (avg = 451.4)
		#
		# examples: 8010653ABB4F13F1 (min size), AAE9D798DC4426DB (max size)

		self.data_size, self.params_count, self.unk2, self.unk3, self.params_batch_end = struct.unpack("<IIIII", data[:20])
		self.textures_count, self.textures_batch_start, self.textures_batch_end, self.unk7, self.unk8 = struct.unpack("<IIIII", data[20:40])

		params_batch = data[40:self.params_batch_end]
		params_keys, params_values = params_batch[:8*self.params_count], params_batch[8*self.params_count:]
		ENTRY_SIZE = 8
		count = self.params_count
		params = [struct.unpack("<HHI", params_keys[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

		self.params = []
		for p in params:
			offset, size, key = p
			self.params += [(key, params_values[offset:offset+size])]

		textures_batch = data[self.textures_batch_start:self.textures_batch_end]
		ENTRY_SIZE = 8
		count = self.textures_count
		self.textures = [struct.unpack("<II", textures_batch[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

		self.strings = data[self.textures_batch_end:] # TODO: use dat1lib.types.sections.StringsSection here?

	"""
	def save(self):
		of = io.BytesIO(bytes())

		self.data_size = self.params_batch_end + self.textures_count * 8 + len(self.strings)

		of.write(struct.pack("<IIIII", self.data_size, self.params_count, self.unk2, self.unk3, self.params_batch_end))
		of.write(struct.pack("<IIIII", self.textures_count, self.textures_batch_start, self.textures_batch_end, self.unk7, self.unk8))
		of.write(self.unk9)		
		for m in self.textures:
			of.write(struct.pack("<II", *m))
		of.write(self.strings)
		of.seek(0)
		return of.read()
	"""

	def get_short_suffix(self):
		return "Material Serialized Data ({}, {})".format(len(self.params), len(self.textures)) # TODO: more like material maps paths? textures paths?

	def _get_string(self, start):
		i = start
		s = bytearray()
		while i < len(self.strings):
			b = self.strings[i]
			if b == 0:
				break
			s.append(b)
			i += 1
		return s.decode('ascii')

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Materials SD |".format(self.TAG))

		print()
		print("         section_size = {}".format(self.data_size))
		print("         unknown 1    = {}".format(self.unk2))
		print("         unknown 2    = {}".format(self.unk3))
		print("         unknown 3    = {}".format(self.unk7))
		print("         unknown 4    = {}".format(self.unk8))

		print()
		print("         // {} parameters (until offset={})".format(self.params_count, self.params_batch_end))
		print()
		#######........ | 123  12345678  ...
		print("           #    slotname  value")
		print("         -----------------------------")
		for i, (k, v) in enumerate(self.params):
			base_line = "         - {:<3}  {:08X}  {}".format(i, k, utils.format_bytes(v))
			prefix = ""

			if k == 0x4BAAD667:
				prefix = "DiffuseColor = {}".format(struct.unpack("<3f", v))

			elif k == 0x24F4CA4C:
				prefix = "Glossiness = {}".format(struct.unpack("<f", v)[0])

			elif k == 0x01876E44:
				prefix = "\"Tiling\" = {}".format(struct.unpack("<f", v)[0])

			if prefix != "":
				prefix = " -- " + prefix

				target_len = 62
				if len(base_line) < target_len:
					prefix = " " * (target_len - len(base_line)) + prefix

			print(base_line + prefix)
		print()

		print()
		print("         // {} textures (from offset={} until offset={})".format(self.textures_count, self.textures_batch_start, self.textures_batch_end))
		print()
		#######........ | 123  12345678  1234  ...
		print("           #    slotname  ofst  value")
		print("         -----------------------------")
		for i in range(len(self.textures)):
			spos, shash = self.textures[i]

			s = self._get_string(spos)
			if s is None:
				s = "<str at {}>".format(spos)

			print("         - {:<3}  {:08X}  {:<4}  {}".format(i, shash, spos, repr(s)))
		print()

#

class xD9B12454_Section(dat1lib.types.sections.Section):
	TAG = 0xD9B12454
	TYPE = 'Material'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 8 occurrences in 13178 files
		# size = 52
		#
		# examples: 891E22BD4A6EA203

		# MM
		# 24 occurrences in 11787 files
		# size = 52
		#
		# examples: 82D70D47FF52BF2F
				
		self.count, self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.texture_c, self.texture_n, self.texture_g, self.texture_c2 = struct.unpack("<I8f4I", data)

	def get_short_suffix(self):
		return "D9B12454"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | D9B12454     |".format(self.TAG))
		print()
		print(" "*8+"   count = {}".format(self.count))
		print(" "*8+"   {:8.3}  {:8.3}  {:8.3}  {:8.3}".format(self.a, self.b, self.c, self.d))
		print(" "*8+"   {:8.3}  {:8.3}  {:8.3}  {:8.3}".format(self.e, self.f, self.g, self.h))
		print(" "*8+"   {}".format(repr(self._dat1.get_string(self.texture_c))))
		print(" "*8+"   {}".format(repr(self._dat1.get_string(self.texture_n))))
		print(" "*8+"   {}".format(repr(self._dat1.get_string(self.texture_g))))
		print(" "*8+"   {}".format(repr(self._dat1.get_string(self.texture_c2))))

#

class x3E45AA13_Section(dat1lib.types.sections.Section):
	TAG = 0x3E45AA13
	TYPE = 'Material'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 3481 occurrences in 13178 files
		# size = 520
		#
		# examples: 8000E61F841EBC5F

		# MM
		# 3429 occurrences in 11787 files
		# size = 520
		#
		# examples: 8000E61F841EBC5F
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "3E45AA13 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 3E45AA13     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xE1275683_Section(dat1lib.types.sections.Section):
	TAG = 0xE1275683
	TYPE = 'Material'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 13178 occurrences in 13178 files (always present)
		# size = 40
		# always first
		#
		# examples: 8000B10F551366C6

		# MM
		# 11787 occurrences in 11787 files (always present)
		# size = 40
		# always first
		#
		# examples: 8000B10F551366C6
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "E1275683 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | E1275683     | {:6} entries".format(self.TAG, len(self.entries)))
