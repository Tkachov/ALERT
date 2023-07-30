import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class LOD(object):
	def __init__(self, data):
		self.start, self.count = struct.unpack("<HH", data)

class Look(object):
	def __init__(self, data):
		self.lods = utils.read_class_array_data(data, 4, LOD)

class ModelLookSection(dat1lib.types.sections.Section):
	TAG = 0x06EB7EFC # Model Look
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 38298 occurrences in 38298 files (always present)
		# size = 32..2080 (avg = 34.1)
		#
		# examples: 800058C35E144B3F (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 37147 occurrences in 37147 files (always present)
		# size = 32..2016 (avg = 34.0)
		#
		# examples: 800058C35E144B3F (min size), AC32788DFEFA4405 (max size)

		# RCRA
		# 11387 occurrences in 11387 files (always present)
		# size = 32..4096 (avg = 41.6)
		#
		# examples: 800102AC251CF360 (min size), 9453965A305B5750 (max size)

		self.looks = utils.read_class_array_data(data, 4*8, Look)

	def get_short_suffix(self):
		return "Model Look ({})".format(len(self.looks))

	def _get_table_as_string(self):
		result = "\n"
		###########........ | 123  123 123  123 123  123 123  123 123  123 123  123 123  123 123  123 123
		result += "           #    LOD0     LOD1     LOD2     LOD3     LOD4     LOD5     LOD6     LOD7   \n"
		result += "         -----------------------------------------------------------------------------\n"
		for i, l in enumerate(self.looks):
			result += "         - {:<3}".format(i)
			for lod in l.lods:
				result += "  {:<3} {:<3}".format(lod.start, lod.count)
			result += "\n"
		result += "\n"
		return result

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Model Look   | {:6} looks".format(self.TAG, len(self.looks)))
		print(self._get_table_as_string())

	def web_repr(self):
		return {"name": "Model Look", "type": "text", "readonly": True, "content": "{} looks:\n{}\n".format(len(self.looks), self._get_table_as_string())}

###

class LookBuilt(object):
	def __init__(self, data):
		self.unknowns = struct.unpack("<16I", data[:64])
		self.count, self.crc32_original, self.crc32_lowercase, self.string_offset = struct.unpack("<IIII", data[64:])

class ModelLookBuiltSection(dat1lib.types.sections.Section):
	TAG = 0x811902D7 # Model Look Built
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 38298 occurrences in 38298 files (always present)
		# size = 1624..108882 (avg = 1749.0)
		#
		# examples: 80032369552B0B62 (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 37147 occurrences in 37147 files (always present)
		# size = 1624..102562 (avg = 1743.3)
		#
		# examples: 80038A947A2C3B00 (min size), AC32788DFEFA4405 (max size)

		# RCRA
		# 11387 occurrences in 11387 files (always present)
		# size = 1624..210514 (avg = 2123.3)
		#
		# examples: 8001C5178A52131F (min size), B5EE7D94C1E5BC7B (max size)

		size1, = struct.unpack("<I", data[:4])
		looks = data[:size1]

		self.looks = utils.read_class_array_data(looks, 80, LookBuilt)
		self.rest = data[size1:] # includes indexes ranges where indexes go from 0 to N, where N is amount of quintuples from 0x0AD3A708

	def get_short_suffix(self):
		return "Model Look Built"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Look Built   |".format(self.TAG))

		print()
		for i, l in enumerate(self.looks):
			look_name = "<offset {}>".format(l.string_offset)
			try:
				name = self._dat1.get_string(l.string_offset)
				if name is not None:
					look_name = name
			except:
				pass

			print("         - {:<3}  {:8}  {:08X}  {:08X}  {}".format(i, l.count, l.crc32_lowercase, l.crc32_original, look_name))
			for i in range(0, 16, 4):
				print("                {:8}  {:8}  {:8}  {:8}".format(l.unknowns[i], l.unknowns[i+1], l.unknowns[i+2], l.unknowns[i+3]))
			print()

		if len(self.rest) > 0:
			print("and {} bytes:".format(len(self.rest)))
			utils.print_bytes_formatted(self.rest, prefix=" "*9)
			print()

###

class xDF9FDF12_Section(dat1lib.types.sections.Section):
	TAG = 0xDF9FDF12
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 38275 occurrences in 38298 files
		# size = 16..1040 (avg = 17.0)
		#
		# examples: 800058C35E144B3F (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 37115 occurrences in 37147 files
		# size = 16..1008 (avg = 16.9)
		#
		# examples: 800058C35E144B3F (min size), AC32788DFEFA4405 (max size)

		# RCRA
		# 11104 occurrences in 11387 files
		# size = 16..1936 (avg = 20.0)
		#
		# examples: 800102AC251CF360 (min size), B5EE7D94C1E5BC7B (max size)

		self.entries = utils.read_struct_array_data(data, "<4I")
		# (0, 70, 0, 2)
		# the same amount of entries as the amount of looks?

	def get_short_suffix(self):
		return "0-70-0-2? ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 0-70-0-2?    | {:6} tuples".format(self.TAG, len(self.entries)))

		print("")
		#######........ | 123  123456  123456  123456  123456
		print("           #         0      70       0       2")
		print("         -------------------------------------")
		for i, l in enumerate(self.entries):
			print("         - {:<3}  {:6}  {:6}  {:6}  {:6}".format(i, l[0], l[1], l[2], l[3]))
		print("")
