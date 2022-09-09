import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

# common with .cinematic2

class x212BD372_Section(dat1lib.types.sections.Section):
	TAG = 0x212BD372
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2174 occurrences in 1683 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24..28416 (avg = 678.9)
		#
		# examples: 80B6332B78CB1955 (min size), 903533D7C4E45412 (max size)
		
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
		return "212BD372 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 212BD372     | {:6} entries".format(self.TAG, len(self.entries))

#

class x6C69A660_Section(dat1lib.types.sections.Section):
	TAG = 0x6C69A660
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2407 occurrences in 1683 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24
		#
		# examples: 8001A078B458EE04
		
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
		return "6C69A660 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 6C69A660     | {:6} entries".format(self.TAG, len(self.entries))

#

class x66CA6C6F_Section(dat1lib.types.sections.Section):
	TAG = 0x66CA6C6F
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1207 occurrences in 1683 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 80..216000 (avg = 5557.7)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)
		
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
		return "66CA6C6F ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 66CA6C6F     | {:6} entries".format(self.TAG, len(self.entries))

#

class xB79CF1D7_Section(dat1lib.types.sections.Section):
	TAG = 0xB79CF1D7
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2175 occurrences in 1683 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24..64872 (avg = 1603.3)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)
		
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
		return "B79CF1D7 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | B79CF1D7     | {:6} entries".format(self.TAG, len(self.entries))

#

class x73CEE17F_Section(dat1lib.types.sections.Section):
	TAG = 0x73CEE17F
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1204 occurrences in 1683 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 96..259200 (avg = 7666.1)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)
		
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
		return "73CEE17F ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 73CEE17F     | {:6} entries".format(self.TAG, len(self.entries))
#

class xA40B51D2_Section(dat1lib.types.sections.Section):
	TAG = 0xA40B51D2
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1207 occurrences in 1683 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 16..43200 (avg = 1111.5)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)
		
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
		return "A40B51D2 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | A40B51D2     | {:6} entries".format(self.TAG, len(self.entries))

#

class x9FD19C20_Section(dat1lib.types.sections.Section):
	TAG = 0x9FD19C20
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 783 occurrences in 1683 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 80..29793232 (avg = 829093.4)
		#
		# examples: 9D2A0B2B472ADED0 (min size), A0D237BF807F8B9F (max size)
		pass

	def get_short_suffix(self):
		return "9FD19C20 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 9FD19C20     | {:6} bytes".format(self.TAG, len(self._raw))
