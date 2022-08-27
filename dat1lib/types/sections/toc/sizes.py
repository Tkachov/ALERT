import dat1lib.types.sections
import io
import struct

class SizeEntry(object):
	def __init__(self, data):
		self.always1, self.value, self.index = struct.unpack("<III", data)

class SizesSection(dat1lib.types.sections.Section):
	TAG = 0x65BCF461
	TYPE = 'toc'

	def __init__(self, data):
		dat1lib.types.sections.Section.__init__(self, data)

		ENTRY_SIZE = 12
		count = len(data)//ENTRY_SIZE
		self.entries = [SizeEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<III", e.always1, e.value, e.index))
		of.seek(0)
		return of.read()
