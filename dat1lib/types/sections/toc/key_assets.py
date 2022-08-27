import dat1lib.types.sections
import io
import struct

class KeyAssetsSection(dat1lib.types.sections.Section):
	TAG = 0x6D921D7B
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
