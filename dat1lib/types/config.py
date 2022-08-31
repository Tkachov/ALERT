import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class Config(object):
	MAGIC = 0x21A56F68

	def __init__(self, f):
		self.magic, self.dat1_size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print "[!] Bad Config magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC)

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def print_info(self, config):
		print "-------"
		print "Config {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "- size   = {}".format(self.dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)
