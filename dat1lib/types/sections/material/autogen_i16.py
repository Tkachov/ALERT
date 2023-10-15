import dat1lib.types.sections
import io
import struct

#

class x5DA317BF_Section(dat1lib.types.sections.Section):
	TAG = 0x5DA317BF
	TYPE = 'Material_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5821 occurrences in 6925 files
		# size = 16..864 (avg = 147.7)
		#
		# examples: 01AF2AD7 (min size), 6254DEE0 (max size)
		
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
		return "5DA317BF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 5DA317BF     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xB967FF7A_Section(dat1lib.types.sections.Section):
	TAG = 0xB967FF7A
	TYPE = 'Material_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 6206 occurrences in 6925 files
		# size = 16..640 (avg = 162.1)
		#
		# examples: 045B0C66 (min size), 5E0A1CAD (max size)
		
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
		return "B967FF7A ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | B967FF7A     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xBDC72826_Section(dat1lib.types.sections.Section):
	TAG = 0xBDC72826
	TYPE = 'Material_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 6779 occurrences in 6925 files
		# size = 12..24 (avg = 23.5)
		#
		# examples: 01AF2AD7 (min size), 000C8FCD (max size)
		
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
		return "BDC72826 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | BDC72826     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xF2DC60EC_Section(dat1lib.types.sections.Section):
	TAG = 0xF2DC60EC
	TYPE = 'Material_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5822 occurrences in 6925 files
		# size = 8..1376 (avg = 187.3)
		#
		# examples: 0524FA2B (min size), 6254DEE0 (max size)
		
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
		return "F2DC60EC ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | F2DC60EC     | {:6} entries".format(self.TAG, len(self.entries)))

