import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

# common with .materialgraph

class x1CAFE804_Section(dat1lib.types.sections.Section):
	TAG = 0x1CAFE804
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4423 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 16..432 (avg = 130.3)
		#
		# examples: 8000E61F841EBC5F (min size), 833688BC03CD8BAB (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "1CAFE804 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 1CAFE804     | {:6} entries".format(self.TAG, len(self.entries))

#

class x45C4F4C0_Section(dat1lib.types.sections.Section):
	TAG = 0x45C4F4C0
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4389 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 8..536 (avg = 167.0)
		#
		# examples: 81FB726316B0A0CA (min size), 83D5CEEBCD8A4609 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "45C4F4C0 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 45C4F4C0     | {:6} entries".format(self.TAG, len(self.entries))

#

class x8C049CCA_Section(dat1lib.types.sections.Section):
	TAG = 0x8C049CCA
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4530 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 400..800 (avg = 523.5)
		#
		# examples: 800BAF6EA093111C (min size), 8000E61F841EBC5F (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "8C049CCA ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 8C049CCA     | {:6} entries".format(self.TAG, len(self.entries))

#

class xA59F667B_Section(dat1lib.types.sections.Section):
	TAG = 0xA59F667B
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4389 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 16..352 (avg = 125.8)
		#
		# examples: 8000E61F841EBC5F (min size), 9FC1F81BF116DE2B (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "A59F667B ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | A59F667B     | {:6} entries".format(self.TAG, len(self.entries))

#

class xBBFC8900_Section(dat1lib.types.sections.Section):
	TAG = 0xBBFC8900
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4530 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 180352..1088640 (avg = 539245.6)
		#
		# examples: A8FE8763415A6F99 (min size), 8E1F4B600684B170 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "BBFC8900 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | BBFC8900     | {:6} entries".format(self.TAG, len(self.entries))

#

class xBC93FB5E_Section(dat1lib.types.sections.Section):
	TAG = 0xBC93FB5E
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4530 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 280..560 (avg = 366.4)
		#
		# examples: 800BAF6EA093111C (min size), 8000E61F841EBC5F (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "BC93FB5E ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | BC93FB5E     | {:6} entries".format(self.TAG, len(self.entries))

#

class xC24B19D9_Section(dat1lib.types.sections.Section):
	TAG = 0xC24B19D9
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 279 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 8..16 (avg = 9.1)
		#
		# examples: 8037745A90D97633 (min size), 81314739879CD24C (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "C24B19D9 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | C24B19D9     | {:6} entries".format(self.TAG, len(self.entries))

#

class xF9C35F30_Section(dat1lib.types.sections.Section):
	TAG = 0xF9C35F30
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2818 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 20
		#
		# examples: 800BAF6EA093111C
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "F9C35F30 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | F9C35F30     | {:6} entries".format(self.TAG, len(self.entries))

#

class xFD113362_Section(dat1lib.types.sections.Section):
	TAG = 0xFD113362
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1751 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 8
		#
		# examples: 800BAF6EA093111C
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "FD113362 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | FD113362     | {:6} entries".format(self.TAG, len(self.entries))
