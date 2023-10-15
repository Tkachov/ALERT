import dat1lib.types.sections
import io
import struct

#

class xADBED8E3_Section(dat1lib.types.sections.Section):
	TAG = 0xADBED8E3
	TYPE = 'Cinematic2_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 350 occurrences in 350 files (always present)
		# size = 50..203276 (avg = 3025.9)
		#
		# examples: 3CAAA304 (min size), A563E049 (max size)
		pass

	def get_short_suffix(self):
		return "ADBED8E3 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | ADBED8E3     | {:6} bytes".format(self.TAG, len(self._raw)))

#

class xBEB60081_Section(dat1lib.types.sections.Section):
	TAG = 0xBEB60081
	TYPE = 'Cinematic2_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 350 occurrences in 350 files (always present)
		# size = 4..336 (avg = 22.7)
		#
		# examples: 02F29443 (min size), 5F4BB9A9 (max size)
		
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
		return "BEB60081 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | BEB60081     | {:6} entries".format(self.TAG, len(self.entries)))

