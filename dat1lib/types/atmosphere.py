import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class Atmosphere(object):
	MAGIC = 0x39F27E27

	def __init__(self, f):
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print "[!] Bad Atmosphere magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC)

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print "-------"
		print "Atmosphere {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.size)
		print "-------"
		print ""

		self.dat1.print_info(config)
