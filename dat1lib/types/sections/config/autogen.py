import dat1lib.types.sections
import io
import struct

class x58B8558A_Section(dat1lib.types.sections.Section):
	TAG = 0x58B8558A
	TYPE = 'Config'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1276 occurrences in 2521 files
		# size = 16..6336 (avg = 100.3)
		#
		# examples: 8008619CBD504B56 (min size), A2E15A1561AF23C6 (max size)
		
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
		return "58B8558A ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 58B8558A     | {:6} entries".format(self.TAG, len(self.entries))
