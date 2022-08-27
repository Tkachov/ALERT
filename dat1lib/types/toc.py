import dat1lib.types.dat1
import io
import struct
import zlib

class TOC(object):
	MAGIC = 0x77AF12AF

	def __init__(self, f):
		self.magic, self.size = struct.unpack("<II", f.read(8))

		if self.magic != self.MAGIC:
			print "[!] Bad 'toc' magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC)
		
		dec = zlib.decompressobj(0)
		data = dec.decompress(f.read())

		if len(data) != self.size:
			print "[!] Actual decompressed size {} isn't equal to one written in the file {}".format(len(data), self.size)

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(data))

	def save(self, f):
		of = io.BytesIO(bytes())
		self.dat1.save(of)
		of.seek(0)
		uncompressed = of.read()

		c = zlib.compressobj()
		compressed = c.compress(uncompressed)
		compressed += c.flush()
		
		f.write(struct.pack("<II", self.magic, len(uncompressed)))
		f.write(compressed)
