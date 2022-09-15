import dat1lib.types.sections
import io
import struct

#

class x4EDE3593_Section(dat1lib.types.sections.Section):
	TAG = 0x4EDE3593
	TYPE = 'Texture'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 25602 occurrences in 25602 files (always present)
		# size = 44
		# always first
		# always last
		#
		# examples: 800035F1EBDCBCEC
		
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
		return "4EDE3593 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 4EDE3593     | {:6} entries".format(self.TAG, len(self.entries))

