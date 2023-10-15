import dat1lib.types.sections
import io
import struct

#

class x16F3BA18_Section(dat1lib.types.sections.Section):
	TAG = 0x16F3BA18
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 8775 occurrences in 8780 files
		# size = 12..2213544 (avg = 16140.1)
		#
		# examples: 2AD6B126 (min size), 7929FC02 (max size)
		
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
		return "16F3BA18 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 16F3BA18     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x237D59F1_Section(dat1lib.types.sections.Section):
	TAG = 0x237D59F1
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 9 occurrences in 8780 files
		# size = 160..12314 (avg = 1888.4)
		#
		# examples: 4FE34225 (min size), 7927C845 (max size)
		pass

	def get_short_suffix(self):
		return "237D59F1 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 237D59F1     | {:6} bytes".format(self.TAG, len(self._raw)))

#

class x5796FEF6_Section(dat1lib.types.sections.Section):
	TAG = 0x5796FEF6
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5166 occurrences in 8780 files
		# size = 10..384190 (avg = 4249.8)
		#
		# examples: 36F6496B (min size), 7929FC02 (max size)
		pass

	def get_short_suffix(self):
		return "5796FEF6 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 5796FEF6     | {:6} bytes".format(self.TAG, len(self._raw)))

#

class x4AD86765_Section(dat1lib.types.sections.Section):
	TAG = 0x4AD86765
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3508 occurrences in 8780 files
		# size = 16..2848 (avg = 254.4)
		#
		# examples: 0078706C (min size), 7E3E18BC (max size)
		
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
		return "4AD86765 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 4AD86765     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x45079BC5_Section(dat1lib.types.sections.Section):
	TAG = 0x45079BC5
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 9 occurrences in 8780 files
		# size = 27888..7305120 (avg = 1185632.0)
		#
		# examples: 4FE34225 (min size), 7927C845 (max size)
		
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
		return "45079BC5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 45079BC5     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xF4CB2F37_Section(dat1lib.types.sections.Section):
	TAG = 0xF4CB2F37
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5166 occurrences in 8780 files
		# size = 18..235590 (avg = 1664.7)
		#
		# examples: 36F6496B (min size), 7929FC02 (max size)
		pass

	def get_short_suffix(self):
		return "F4CB2F37 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | F4CB2F37     | {:6} bytes".format(self.TAG, len(self._raw)))
