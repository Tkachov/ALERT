import dat1lib.types.sections
import io
import struct

#

class x06A58050_Section(dat1lib.types.sections.Section):
	TAG = 0x06A58050
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 229472
		#
		# examples: BE55D94F171BF8DE
		
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
		return "06A58050 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 06A58050     | {:6} entries".format(self.TAG, len(self.entries))

#

class x0CD2CFE9_Section(dat1lib.types.sections.Section):
	TAG = 0x0CD2CFE9
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 114736
		#
		# examples: BE55D94F171BF8DE
		
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
		return "0CD2CFE9 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 0CD2CFE9     | {:6} entries".format(self.TAG, len(self.entries))

#

class x4D73CEBD_Section(dat1lib.types.sections.Section):
	TAG = 0x4D73CEBD
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 1348825
		#
		# examples: BE55D94F171BF8DE
		pass

	def get_short_suffix(self):
		return "4D73CEBD ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 4D73CEBD     | {:6} bytes".format(self.TAG, len(self._raw))

#

class x70A382B8_Section(dat1lib.types.sections.Section):
	TAG = 0x70A382B8
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 3039405..4903208 (avg = 3404552.5)
		# always last
		#
		# examples: BE55D94F171BF8DE (min size), BE55D94F171BF8DE (max size)
		pass

	def get_short_suffix(self):
		return "70A382B8 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 70A382B8     | {:6} bytes".format(self.TAG, len(self._raw))

#

class xA4EA55B2_Section(dat1lib.types.sections.Section):
	TAG = 0xA4EA55B2
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 229472
		#
		# examples: BE55D94F171BF8DE
		
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
		return "A4EA55B2 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | A4EA55B2     | {:6} entries".format(self.TAG, len(self.entries))

#

class xB0653243_Section(dat1lib.types.sections.Section):
	TAG = 0xB0653243
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 229472
		#
		# examples: BE55D94F171BF8DE
		
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
		return "B0653243 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | B0653243     | {:6} entries".format(self.TAG, len(self.entries))

#

class xC43731B5_Section(dat1lib.types.sections.Section):
	TAG = 0xC43731B5
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 229472
		#
		# examples: BE55D94F171BF8DE
		
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
		return "C43731B5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | C43731B5     | {:6} entries".format(self.TAG, len(self.entries))

#

class xD540A903_Section(dat1lib.types.sections.Section):
	TAG = 0xD540A903
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 4
		# always first
		#
		# examples: BE55D94F171BF8DE
		
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
		return "D540A903 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | D540A903     | {:6} entries".format(self.TAG, len(self.entries))

#

class xF80DEEB4_Section(dat1lib.types.sections.Section):
	TAG = 0xF80DEEB4
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 229472
		#
		# examples: BE55D94F171BF8DE
		
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
		return "F80DEEB4 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | F80DEEB4     | {:6} entries".format(self.TAG, len(self.entries))
