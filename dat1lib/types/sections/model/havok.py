import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class HavokStruct(object):
	def __init__(self, f):
		self.magic = f.read(1)
		self.len = (f.read(1)[0] << 16)
		self.len |= (f.read(1)[0] << 8)
		self.len |= (f.read(1)[0])
		self.name = f.read(4)
		if self.len > 8:
			self.data = f.read(self.len - 8)

class HavokBigStruct(object):
	def __init__(self, f):
		startpos = f.tell()		
		self.size, = struct.unpack(">I", f.read(4))
		self.name = f.read(4)
		self.structs = []
		while f.tell() < startpos + self.size:
			self.structs += [HavokStruct(f)]

class HavokData(object):
	def __init__(self, f):
		self.size, = struct.unpack(">I", f.read(4))
		self.magic = f.read(4)
		self.version = HavokStruct(f)
		self.data_struct = HavokStruct(f)
		self.structs = []
		while f.tell() < self.size:
			self.structs += [HavokBigStruct(f)]
		self.leftover = f.read()

class HavokSection(dat1lib.types.sections.Section):
	TAG = 0xEFD92E68 # Model Physics Data
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 9987 occurrences in 38298 files
		# size = 1976..349824 (avg = 16819.7)
		#
		# examples: 800804287BB19C92 (min size), 8FFC77E5D7F22334 (max size)

		# MM
		# 10370 occurrences in 37147 files
		# size = 1976..474756 (avg = 16549.3)
		#
		# examples: 8020C5A0E811B1F7 (min size), 8C7796FC7478109D (max size)

		self.data = HavokData(io.BytesIO(data))

	def get_short_suffix(self):
		return "havok"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Havok Data   |".format(self.TAG))

	def web_repr(self):
		return {"name": "Havok Data", "type": "text", "readonly": True, "content": ""}
