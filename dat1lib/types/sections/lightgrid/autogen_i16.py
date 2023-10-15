import dat1lib.types.sections
import io
import struct

#

class x96D77BBD_Section(dat1lib.types.sections.Section):
	TAG = 0x96D77BBD
	TYPE = 'LightGrid_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 40393 occurrences in 46816 files
		# size = 4..108 (avg = 26.5)
		#
		# examples: 00443A83 (min size), BD2F1379 (max size)
		
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
		return "96D77BBD ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 96D77BBD     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x9989BB49_Section(dat1lib.types.sections.Section):
	TAG = 0x9989BB49
	TYPE = 'LightGrid_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 46816 occurrences in 46816 files (always present)
		# size = 98304
		# always first
		#
		# examples: 00011946
		
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
		return "9989BB49 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 9989BB49     | {:6} entries".format(self.TAG, len(self.entries)))

