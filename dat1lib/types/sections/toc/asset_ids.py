import dat1lib.types.sections
import io
import struct

class AssetIdsSection(dat1lib.types.sections.Section):
	TAG = 0x506D7B8A
	TYPE = 'toc'

	def __init__(self, data):
		dat1lib.types.sections.Section.__init__(self, data)

		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.ids = [struct.unpack("<Q", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for aid in self.ids:
			of.write(struct.pack("<Q", aid))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "asset ids ({})".format(len(self.ids))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Asset IDs    | {:6} entries".format(self.TAG, len(self.ids))
