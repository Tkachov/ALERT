import dat1lib.types.sections
import io
import struct

#

class x2F4056CE_Section(dat1lib.types.sections.Section):
	TAG = 0x2F4056CE
	TYPE = 'Conduit'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 708 occurrences in 1234 files
		# size = 16..1728 (avg = 71.3)
		#
		# examples: 80035676415E24D6 (min size), AF207C743E768578 (max size)
		
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
		return "2F4056CE ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2F4056CE     | {:6} entries".format(self.TAG, len(self.entries))

#

class xCEB30E68_Section(dat1lib.types.sections.Section):
	TAG = 0xCEB30E68
	TYPE = 'Conduit'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1234 occurrences in 1234 files (always present)
		# size = 72..522232 (avg = 13505.9)
		# always first
		#
		# examples: 93D2FB47CF888B46 (min size), AF207C743E768578 (max size)
		
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
		return "CEB30E68 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | CEB30E68     | {:6} entries".format(self.TAG, len(self.entries))

