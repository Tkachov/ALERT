import dat1lib.types.sections
import io
import struct

class KeyAssetsSection(dat1lib.types.sections.Section):
	TAG = 0x6D921D7B
	TYPE = 'toc'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.ids = [struct.unpack("<Q", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for aid in self.ids:
			of.write(struct.pack("<Q", aid))
		of.seek(0)
		return bytearray(of.read())

	def get_short_suffix(self):
		return "key assets ({})".format(len(self.ids))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Key Assets   | {:6} entries".format(self.TAG, len(self.ids)))
