import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class JointsMapSection(dat1lib.types.sections.UintUintMapSection):
	TAG = 0xEE31971C # Model Joint Lookup
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.UintUintMapSection.__init__(self, data, container)

		# MSMR
		# 2311 occurrences in 38298 files
		# size = 16..25416 (avg = 458.6)
		#
		# examples: 800804287BB19C92 (min size), BBCAFC4308D39DEC (max size)

		# MM
		# 2004 occurrences in 37147 files
		# size = 16..25072 (avg = 384.9)
		#
		# examples: 800B08BE9B0E1249 (min size), B699EAFFCD4834D0 (max size)

		# RCRA
		# 1123 occurrences in 11387 files
		# size = 16..19480 (avg = 256.6)
		#
		# examples: 80116594638FB4B9 (min size), 80F95D8660F364D7 (max size)

	def get_short_suffix(self):
		return "joints map ({})".format(len(self._map))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Joints Map   | {:6} joints".format(self.TAG, len(self._map)))

	def web_repr(self):
		return {"name": "Model Joint Lookup", "type": "text", "readonly": True, "content": "(see 15DF9D3B for index/hash mapping)"}

###

class JointDefinition(object):
	def __init__(self, data):
		self.parent, self.index, self.unknown1, self.unknown2, self.hash, self.string_offset = struct.unpack("<hHHHII", data)
		# hash = crc32(name, normalize=False), that is, without lower() (which, however, is used for material names)
		# parent is -1 if none
		# unknown1 is amount of "children" (not only direct, but all in hierarchy) of this joint?
		# unknown2 some flags? type of joint?

class JointsSection(dat1lib.types.sections.Section):
	TAG = 0x15DF9D3B # Model Joint
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2311 occurrences in 38298 files
		# size = 16..50816 (avg = 901.2)
		#
		# examples: 800804287BB19C92 (min size), BBCAFC4308D39DEC (max size)

		# MM
		# 2004 occurrences in 37147 files
		# size = 16..50128 (avg = 753.9)
		#
		# examples: 800B08BE9B0E1249 (min size), B699EAFFCD4834D0 (max size)

		# RCRA
		# 1123 occurrences in 11387 files
		# size = 16..38944 (avg = 497.3)
		#
		# examples: 80116594638FB4B9 (min size), 80F95D8660F364D7 (max size)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.joints = [JointDefinition(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def get_short_suffix(self):
		return "joints ({})".format(len(self.joints))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Joint Defs   | {:6} joints".format(self.TAG, len(self.joints)))

		print("")
		#######........ | 123  12345678  12345678901234567890123456789012  1234  1234  1234  1234
		print("           #        hash  name                            parent   ndx     ?     ?")
		print("         -------------------------------------------------------------------------")
		for i, l in enumerate(self.joints):
			name = self._dat1.get_string(l.string_offset)

			print("         - {:<3}  {:08X}  {}{}  {:4}  {:4}  {:4}  {:4}".format(i, l.hash, name[:32], " "*(32 - len(name[:32])), l.parent, l.index, l.unknown1, l.unknown2))
			if config.get("section_warnings", True):
				nhsh = crc32.hash(name, False)
				if nhsh != l.hash:
					print("        [!] name real hash {:08X} is not equal to one written in the struct {:08X}".format(nhsh, l.hash))

		print("")

###

class xDCC88A19_Section(dat1lib.types.sections.Section):
	TAG = 0xDCC88A19
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2311 occurrences in 38298 files
		# size = 128..355712 (avg = 6332.5)
		#
		# examples: 800804287BB19C92 (min size), BBCAFC4308D39DEC (max size)

		# MM
		# 2004 occurrences in 37147 files
		# size = 128..350912 (avg = 5300.5)
		#
		# examples: 800B08BE9B0E1249 (min size), B699EAFFCD4834D0 (max size)

		# RCRA
		# 1123 occurrences in 11387 files
		# size = 128..272640 (avg = 3501.9)
		#
		# examples: 80116594638FB4B9 (min size), 80F95D8660F364D7 (max size)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.vectors = [struct.unpack("<ffff", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def get_short_suffix(self):
		return "vectors? ({})".format(len(self.vectors))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Vectors?     | {:6} vectors".format(self.TAG, len(self.vectors)))
		# TODO: print(vec4f)

###

class xB7380E8C_Section(dat1lib.types.sections.Section):
	TAG = 0xB7380E8C
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2311 occurrences in 38298 files
		# size = 2..6346 (avg = 79.1)
		#
		# examples: 800804287BB19C92 (min size), BBCAFC4308D39DEC (max size)

		# MM
		# 2004 occurrences in 37147 files
		# size = 2..6264 (avg = 65.3)
		#
		# examples: 8008B62FF6E72FDE (min size), B699EAFFCD4834D0 (max size)

		# RCRA
		# 1123 occurrences in 11387 files
		# size = 2..4866 (avg = 31.7)
		#
		# examples: 80116594638FB4B9 (min size), 80F95D8660F364D7 (max size)

		# some unique numbers from 0, but with some gaps
		# for example, 146 numbers from 0 up to 220
		self.indexes = utils.read_struct_N_array_data(data, len(data)//2, "<H")

	def get_short_suffix(self):
		return "indexes? ({})".format(len(self.indexes))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Some Indexes | {:6} indexes".format(self.TAG, len(self.indexes)))

###

class xC5354B60_Section(dat1lib.types.sections.Section):
	TAG = 0xC5354B60 # Model Mirror Ids
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2311 occurrences in 38298 files
		# size = 4..12704 (avg = 182.0)
		#
		# examples: 800804287BB19C92 (min size), BBCAFC4308D39DEC (max size)

		# MM
		# 2004 occurrences in 37147 files
		# size = 4..12532 (avg = 153.3)
		#
		# examples: 800B08BE9B0E1249 (min size), B699EAFFCD4834D0 (max size)

		# RCRA
		# 1123 occurrences in 11387 files
		# size = 4..9736 (avg = 93.7)
		#
		# examples: 80116594638FB4B9 (min size), 80F95D8660F364D7 (max size)

		# some offset-like numbers in "mostly" increasing order
		# (sometimes value returns back to a smaller number and continues to increase)
		self.offsets = utils.read_struct_N_array_data(data, len(data)//4, "<I")

	def get_short_suffix(self):
		return "offsets? ({})".format(len(self.offsets))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Some Offsets | {:6} offsets".format(self.TAG, len(self.offsets)))

#

class x90CDB60C_Section(dat1lib.types.sections.Section):
	TAG = 0x90CDB60C
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2311 occurrences in 38298 files
		# size = 80
		#
		# examples: 8007367BDC86C66B

		# MM
		# 2004 occurrences in 37147 files
		# size = 80
		#
		# examples: 8008B62FF6E72FDE

		# RCRA
		# 1123 occurrences in 11387 files
		# size = 80
		#
		# examples: 80028A780883AD15
		
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
		return "90CDB60C ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 90CDB60C     | {:6} entries".format(self.TAG, len(self.entries)))
