import dat1lib.types.dat1
import io
import struct
import zlib

class DAG(object):
	MAGIC = 0x891F77AF

	def __init__(self, f):
		self.magic, self.size, self.unk1 = struct.unpack("<III", f.read(12))

		if self.magic != self.MAGIC:
			print "[!] Bad 'dag' magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC)
		
		dec = zlib.decompressobj(0)
		data = dec.decompress(f.read())

		if len(data) != self.size:
			print "[!] Actual decompressed size {} isn't equal to one written in the file {}".format(len(data), self.size)

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(data), self)

	def print_info(self, config):
		print "-------"
		print "DAG {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "-------"
		print ""

		self.dat1.print_info(config)
