import dat1lib.types.sections
import io
import struct

#

class x0A6B24F8_Section(dat1lib.types.sections.Section):
	TAG = 0x0A6B24F8
	TYPE = 'ModelVariant_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2 occurrences in 2 files (always present)
		# size = 17224..17276 (avg = 17250.0)
		# always first
		#
		# examples: 915165CD (min size), 06703DB9 (max size)
		
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
		return "0A6B24F8 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 0A6B24F8     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x32FFEA36_Section(dat1lib.types.sections.Section):
	TAG = 0x32FFEA36
	TYPE = 'ModelVariant_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2 occurrences in 2 files (always present)
		# size = 12..16 (avg = 14.0)
		# always last
		#
		# examples: 915165CD (min size), 06703DB9 (max size)
		
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
		return "32FFEA36 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 32FFEA36     | {:6} entries".format(self.TAG, len(self.entries)))

