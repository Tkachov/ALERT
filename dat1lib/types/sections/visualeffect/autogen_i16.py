import dat1lib.types.sections
import io
import struct

#

class x01670690_Section(dat1lib.types.sections.Section):
	TAG = 0x01670690
	TYPE = 'VisualEffect_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3 occurrences in 2348 files
		# size = 16..48 (avg = 26.6)
		#
		# examples: 7172C986 (min size), 327F8C96 (max size)
		
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
		return "01670690 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 01670690     | {:6} entries".format(self.TAG, len(self.entries)))
