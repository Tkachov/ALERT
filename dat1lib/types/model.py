import dat1lib.types.dat1
import io
import struct

class Model(object):
	MAGIC = 0x98906B9F

	def __init__(self, f):
		self.magic, self.offset_to_stream_sections, self.stream_sections_size = struct.unpack("<III", f.read(12))
		self.unk = f.read(24)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print "[!] Bad Model magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC)

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1))

	def save(self, f):
		offset_to_indexbuf = 0
		for s in self.dat1.header.sections:
			if s.tag == 0x0859863D:
				offset_to_indexbuf = s.offset

		self.offset_to_stream_sections = offset_to_indexbuf
		self.stream_sections_size = self.dat1.header.size - offset_to_indexbuf

		f.write(struct.pack("<III", self.magic, self.offset_to_stream_sections, self.stream_sections_size))
		f.write(self.unk)
		self.dat1.save(f)
