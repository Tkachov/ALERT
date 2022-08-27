import dat1lib.types.sections
import io
import struct

class OffsetEntry(object):
	def __init__(self, data):
		self.archive_index, self.offset = struct.unpack("<II", data)

class OffsetsSection(dat1lib.types.sections.Section):
	TAG = 0xDCD720B5
	TYPE = 'toc'

	def __init__(self, data):
		dat1lib.types.sections.Section.__init__(self, data)

		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.entries = [OffsetEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<II", e.archive_index, e.offset))
		of.seek(0)
		return of.read()
