import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class Config(object):
	MAGIC = 0x21A56F68
	EMPTY_DATA = struct.pack("<II", 0x21A56F68, len(dat1lib.types.dat1.DAT1.EMPTY_DATA)) + '\0'*28 + dat1lib.types.dat1.DAT1.EMPTY_DATA

	def __init__(self, f):
		self.magic, self.dat1_size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print "[!] Bad Config magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC)

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	@classmethod
	def make(cls):
		r = cls(io.BytesIO(cls.EMPTY_DATA))
		r.dat1.header.unk1 = cls.MAGIC
		r.dat1.add_string("Config Built File")
		return r

	def save(self, f):
		self.dat1.full_refresh()

		f.write(struct.pack("<II", self.magic, self.dat1.header.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print "-------"
		print "Config {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "- size   = {}".format(self.dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)
