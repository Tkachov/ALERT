import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class HeaderSection(dat1lib.types.sections.Section):
	TAG = 0x02F06D4E
	TYPE = 'atmosphere'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 16 occurrences in 16 files (always present)
		# size = 131552
		# always first
		#
		# examples: 00B27A40

		# MSMR
		# 133 occurrences in 133 files (always present)
		# size = 1576
		# always first
		#
		# examples: 803D388D02427C63

		# MM
		# 108 occurrences in 108 files (always present)
		# size = 1576
		# always first
		#
		# examples: 805D8409A8286E3F

		# RCRA
		# 95 occurrences in 95 files (always present)
		# size = 1800
		# always first
		#
		# examples: 803DF93468026616

		self.unk1 = data[:32]
		self.z1, self.time_of_day, self.z2, self.z3 = struct.unpack("<IfII", data[32:48])
		self.unk2 = data[48:64]
		self.pairs = [struct.unpack("<ff", data[72+i*8:72+(i+1)*8]) for i in range(6)]
		self.sun_rgba = struct.unpack("<ffff", data[112:128])
		self.sun_rot, self.sun_elev = struct.unpack("<ff", data[128:136])
		self.a, self.b, self.c, self.sun_radius = struct.unpack("<IIfI", data[136:152])
		self.unk3 = struct.unpack("<" + "f"*5 + "i" + "f"*4, data[152:192])
		self.ambience_rgba = struct.unpack("<ffff", data[192:208])

	def get_short_suffix(self):
		return "header"
		# return "events ({})".format(len(self.events))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Header       |".format(self.TAG))
		print(self.time_of_day)
		print(["{} {}".format(*c) for c in self.pairs])
		print("{} {} {}".format(self.sun_rgba, self.sun_rot, self.sun_elev))
		print("{} {} {} {}".format(self.a, self.b, self.c, self.sun_radius)) # "{:08X}".format(self.c)
		print(self.unk3)
		print(self.ambience_rgba)

###

class StringsSection(dat1lib.types.sections.StringsSection):
	TAG = 0x72F28658
	TYPE = 'atmosphere'

	def __init__(self, data, container):
		dat1lib.types.sections.StringsSection.__init__(self, data, container)

		# MSMR
		# 127 occurrences in 133 files
		# size = 1..88 (avg = 63.8)
		#
		# examples: 8814BE4101361FCC (min size), B11F882525900C32 (max size)

		# MM
		# 106 occurrences in 108 files
		# size = 1..87 (avg = 51.4)
		#
		# examples: 93D0C8E529805B2C (min size), 80BA05E01E62AE5B (max size)

		# RCRA
		# 92 occurrences in 95 files
		# size = 33..85 (avg = 55.0)
		#
		# examples: 9C31C1274367139B (min size), B125D81B2F3D3024 (max size)

	def get_short_suffix(self):
		return "strings ({})".format(len(self._strings))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Strings      | {:6} strings".format(self.TAG, len(self._strings)))
		for s in self._strings:
			print(" "*11 + "- '{}'".format(s))
			#print(" "*13 + "{:08X} {:08X} {:016X}".format(crc32.hash(s+'\x00'), crc32.hash(s+'\x00', False), crc64.hash(s+'\x00')))
		print("")

###

class TextureSection(dat1lib.types.sections.Section):
	TAG = 0x71C168B4
	TYPE = 'atmosphere'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 120 occurrences in 133 files
		# size = 524268
		#
		# examples: 803D388D02427C63

		# MM
		# 101 occurrences in 108 files
		# size = 524268..2096748 (avg = 539837.1)
		#
		# examples: 805D8409A8286E3F (min size), 970D43801CB614DC (max size)

		# RCRA
		# 92 occurrences in 95 files
		# size = 108
		#
		# examples: 803DF93468026616

	def get_short_suffix(self):
		return "texture DAT1"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Texture DAT1 |".format(self.TAG))

###

class xE7997256_Section(dat1lib.types.sections.Section):
	TAG = 0xE7997256
	TYPE = 'atmosphere'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 16 occurrences in 16 files (always present)
		# size = 2244624
		# always last
		#
		# examples: 00B27A40

		# MSMR
		# 66 occurrences in 133 files
		# size = 2244624
		#
		# examples: 80BA05E01E62AE5B

		# MM
		# 27 occurrences in 108 files
		# size = 2244624
		#
		# examples: 80BA05E01E62AE5B

		# RCRA
		# 13 occurrences in 95 files
		# size = 2244624
		#
		# examples: 8230BE9511D6C9EB
		
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
		return "? ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | ?            | {:6} entries".format(self.TAG, len(self.entries)))
