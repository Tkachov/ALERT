import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class UnknownAsset(object):
	def __init__(self, f):
		self.magic, self.likely_is_dat1_size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def print_info(self, config):
		print "-------"
		print "Asset? {:08X}".format(self.magic)
		print "- size?  = {}".format(self.likely_is_dat1_size)
		utils.print_bytes_formatted([ord(c) for c in self.unk], "- ", 2)
		print "-------"
		print ""

		self.dat1.print_info(config)
