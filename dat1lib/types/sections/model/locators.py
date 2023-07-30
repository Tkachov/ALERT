import dat1lib.crc32 as crc32
import dat1lib.types.sections
import io
import struct

class LocatorsMapSection(dat1lib.types.sections.UintUintMapSection):
	TAG = 0x731CBC2E # Model Locator Lookup
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.UintUintMapSection.__init__(self, data, container)

		# MSMR
		# 1401 occurrences in 38298 files
		# size = 8..2944 (avg = 312.4)
		#
		# examples: 8008B62FF6E72FDE (min size), 8BBCF107882FAD67 (max size)

		# MM
		# 1177 occurrences in 37147 files
		# size = 8..2696 (avg = 283.6)
		#
		# examples: 8008B62FF6E72FDE (min size), B742D90D7B153BDF (max size)

		# RCRA
		# 580 occurrences in 11387 files
		# size = 8..2816 (avg = 139.6)
		#
		# examples: 8046DF89E57B13AA (min size), AAD40A235F0953CE (max size)

	def get_short_suffix(self):
		return "locators map ({})".format(len(self._map))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Locators Map | {:6} locators".format(self.TAG, len(self._map)))

	def web_repr(self):
		return {"name": "Model Locator Lookup", "type": "text", "readonly": True, "content": "(see 9F614FAB for index/hash mapping)"}

###

class LocatorDefinition(object):
	def __init__(self, data):
		self.hash, self.string_offset, self.joint, self.zero = struct.unpack("<IIiI", data[:16])
		# hash = crc32(name, normalize=False), that is, without lower() (which, however, is used for material names)
		# joint is -1 if none

		self.matrix = [
			struct.unpack("<fff", data[16:28]),
			struct.unpack("<fff", data[28:40]),
			struct.unpack("<fff", data[40:52]),
			struct.unpack("<fff", data[52:64])
		]
		"""
		1 0 0
		0 1 0
		0 0 1
		0 0 0, for example
		"""

class LocatorsSection(dat1lib.types.sections.Section):
	TAG = 0x9F614FAB # Model Locator
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 1401 occurrences in 38298 files
		# size = 64..23552 (avg = 2499.7)
		#
		# examples: 8008B62FF6E72FDE (min size), 8BBCF107882FAD67 (max size)

		# MM
		# 1177 occurrences in 37147 files
		# size = 64..21568 (avg = 2269.5)
		#
		# examples: 8008B62FF6E72FDE (min size), B742D90D7B153BDF (max size)

		# RCRA
		# 580 occurrences in 11387 files
		# size = 64..22528 (avg = 1117.2)
		#
		# examples: 8046DF89E57B13AA (min size), AAD40A235F0953CE (max size)

		ENTRY_SIZE = 64
		count = len(data)//ENTRY_SIZE
		self.locators = [LocatorDefinition(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def get_short_suffix(self):
		return "locators ({})".format(len(self.locators))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Locator Defs | {:6} locators".format(self.TAG, len(self.locators)))

		print("")
		#######........ | 123  12345678  12345678901234567890123456789012  1234  1234
		print("           #        hash  name                             joint  zero")
		print("         -------------------------------------------------------------")
		for i, l in enumerate(self.locators):
			name = self._dat1.get_string(l.string_offset)

			print("         - {:<3}  {:08X}  {}{}  {:4}  {:4}".format(i, l.hash, name[:32], " "*(32 - len(name[:32])), l.joint, l.zero))
			if config.get("section_warnings", True):
				nhsh = crc32.hash(name, False)
				if nhsh != l.hash:
					print("        [!] name real hash {:08X} is not equal to one written in the struct {:08X}".format(nhsh, l.hash))

		print("")

###

class LocatorRelatedSection(dat1lib.types.sections.Section):
	TAG = 0x9A434B29
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 39 occurrences in 38298 files
		# size = 608..1152 (avg = 914.8)
		#
		# examples: 80C52396F2470510 (min size), 8308C60D2DCEA858 (max size)

		# MM
		# 40 occurrences in 37147 files
		# size = 608..1152 (avg = 716.8)
		#
		# examples: 80C52396F2470510 (min size), 81CDD58B0A93CCE2 (max size)

		# RCRA
		# 7 occurrences in 11387 files
		# size = 608..1648 (avg = 1085.7)
		#
		# examples: A278EE4BEE9C6507 (min size), 9BA94D1544DB197D (max size)

		# TODO: only 39 models, and I've met one of these! maybe hero-related?

		self.size, = struct.unpack("<I", data[:4]) # same as len(data)
		self.unknown1, = struct.unpack("<I", data[4:8]) # always 32?
		self.unknown2, = struct.unpack("<I", data[8:12]) # small
		self.unknown3, = struct.unpack("<I", data[12:16]) # small, approx. *2 of unknown2

		ENTRY_SIZE = 8
		count = (len(data) - 16)//ENTRY_SIZE
		pairs_data = data[16:]
		self.pairs = [struct.unpack("<II", pairs_data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def get_short_suffix(self):
		return "locators info ({})".format(len(self.pairs))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Locator Info | {:6} pairs".format(self.TAG, len(self.pairs)))

	def web_repr(self):
		content =  "size={}\n".format(self.size)
		content += "   a={}\n".format(self.unknown1)
		content += "   b={}\n".format(self.unknown2)
		content += "   c={}\n".format(self.unknown3)
		content += "\n"
		content += "{} pairs".format(len(self.pairs))
		content += "\n"
		############........ | 123  12345678  12345678
		content += "           #           k         v\n"
		content += "         -------------------------\n"
		for i, x in enumerate(self.pairs):
			content += "         - {:<3}  {:08X}  {:08X}\n".format(i, *x)
		content += "\n"
		return {"name": "Locators-related Info", "type": "text", "readonly": True, "content": content}
