import dat1lib.types.sections
import io
import struct

#

class x135832C8_Section(dat1lib.types.sections.Section):
	TAG = 0x135832C8
	TYPE = 'Actor'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4301 occurrences in 5167 files
		# size = 32..1056 (avg = 115.8)
		#
		# examples: 8012CEC29FE92381 (min size), 88EBA704687556DC (max size)
		
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
		return "135832C8 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 135832C8     | {:6} entries".format(self.TAG, len(self.entries))

#

class x32FAC8E0_Section(dat1lib.types.sections.Section):
	TAG = 0x32FAC8E0
	TYPE = 'Actor'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5167 occurrences in 5167 files (always present)
		# size = 4
		# always first
		#
		# examples: 80029DC4DB44B189
		
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
		return "32FAC8E0 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return

		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 32FAC8E0     | {:6} entries".format(self.TAG, len(self.entries))

#

class x364A6C7C_Section(dat1lib.types.sections.Section):
	TAG = 0x364A6C7C
	TYPE = 'Actor'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5167 occurrences in 5167 files (always present)
		# size = 176..320 (avg = 301.3)
		#
		# examples: 802A792FD6F72CE3 (min size), 80029DC4DB44B189 (max size)
		
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
		return "364A6C7C ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return

		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 364A6C7C     | {:6} entries".format(self.TAG, len(self.entries))

#

class x3AB204B9_Section(dat1lib.types.sections.Section):
	TAG = 0x3AB204B9
	TYPE = 'Actor'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4928 occurrences in 5167 files
		# size = 16..2336 (avg = 101.9)
		#
		# examples: 8012CEC29FE92381 (min size), BAAE788E4A9CE960 (max size)
		
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
		return "3AB204B9 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return

		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 3AB204B9     | {:6} entries".format(self.TAG, len(self.entries))

#

class x6D4301EF_Section(dat1lib.types.sections.Section):
	TAG = 0x6D4301EF
	TYPE = 'Actor'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3506 occurrences in 5167 files
		# size = 32..30224 (avg = 1711.7)
		#
		# examples: 8074615B5D3B13A8 (min size), B93103E693B0C988 (max size)
		
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
		return "6D4301EF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return

		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 6D4301EF     | {:6} entries".format(self.TAG, len(self.entries))

