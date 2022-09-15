import dat1lib.types.sections
import io
import struct

#

class x1F6A31A6_Section(dat1lib.types.sections.Section):
	TAG = 0x1F6A31A6
	TYPE = 'LevelLight'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5 occurrences in 5 files (always present)
		# size = 36
		# always first
		#
		# examples: 83F4B7E7E9672F27
		
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
		return "1F6A31A6 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 1F6A31A6     | {:6} entries".format(self.TAG, len(self.entries))

#

class x46EFD07A_Section(dat1lib.types.sections.Section):
	TAG = 0x46EFD07A
	TYPE = 'LevelLight'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5 occurrences in 5 files (always present)
		# size = 16
		# always last
		#
		# examples: 83F4B7E7E9672F27
		
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
		return "46EFD07A ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 46EFD07A     | {:6} entries".format(self.TAG, len(self.entries))

