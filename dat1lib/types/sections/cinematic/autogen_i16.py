import dat1lib.types.sections
import io
import struct

#

class x3C9CB5BF_Section(dat1lib.types.sections.Section):
	TAG = 0x3C9CB5BF
	TYPE = 'Cinematic_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2 occurrences in 2 files (always present)
		# size = 448..3816 (avg = 2132.0)
		# always first
		#
		# examples: 34C9DD49 (min size), 15625880 (max size)
		
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
		return "3C9CB5BF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 3C9CB5BF     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x8075D750_Section(dat1lib.types.sections.Section):
	TAG = 0x8075D750
	TYPE = 'Cinematic_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2 occurrences in 2 files (always present)
		# size = 4
		# always last
		#
		# examples: 15625880
		
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
		return "8075D750 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 8075D750     | {:6} entries".format(self.TAG, len(self.entries)))

