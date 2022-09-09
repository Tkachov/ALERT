import dat1lib.types.sections
import io
import struct

#

class x42F16D0C_Section(dat1lib.types.sections.Section):
	TAG = 0x42F16D0C
	TYPE = 'AnimSet_PerformanceSet'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 499 occurrences in 1683 files
		# size = 96..107040 (avg = 7291.3)
		#
		# examples: 96AD98C8AC61B09A (min size), A8052A228EF425FE (max size)
		
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
		return "42F16D0C ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 42F16D0C     | {:6} entries".format(self.TAG, len(self.entries))

#

class xC8CE8D96_Section(dat1lib.types.sections.Section):
	TAG = 0xC8CE8D96
	TYPE = 'AnimSet_PerformanceSet'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 320 occurrences in 1683 files
		# size = 24..253032 (avg = 3152.7)
		#
		# examples: 81C13ECB778F64AD (min size), 9B4C33CE8CA86160 (max size)
		
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
		return "C8CE8D96 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | C8CE8D96     | {:6} entries".format(self.TAG, len(self.entries))

#

class xD614B18B_Section(dat1lib.types.sections.Section):
	TAG = 0xD614B18B
	TYPE = 'AnimSet_PerformanceSet'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 499 occurrences in 1683 files
		# size = 48..96 (avg = 52.8)
		#
		# examples: 80176C7A46F8A544 (min size), 817AFFAD64BE2622 (max size)
		
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
		return "D614B18B ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | D614B18B     | {:6} entries".format(self.TAG, len(self.entries))

#

class xDF74DA06_Section(dat1lib.types.sections.Section):
	TAG = 0xDF74DA06
	TYPE = 'AnimSet_PerformanceSet'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 134 occurrences in 1683 files
		# size = 12..4992 (avg = 189.0)
		#
		# examples: 80B6332B78CB1955 (min size), 888DBF4798E4E906 (max size)
		
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
		return "DF74DA06 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | DF74DA06     | {:6} entries".format(self.TAG, len(self.entries))

