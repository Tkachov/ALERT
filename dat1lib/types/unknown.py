import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

# .movie = BIK
# .zonelightbin = strange 1TAD/asset, 38 bytes asset header instead of 36

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

#

class LevelLight(UnknownAsset):
	MAGIC = 0x567CC2F0

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "LevelLight {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class Actor(UnknownAsset):
	MAGIC = 0x7C207220

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "Actor {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class AnimClip_PerformanceClip(UnknownAsset):
	MAGIC = 0xC96F58F3

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "AnimClip/PerformanceClip {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class AnimSet_PerformanceSet(UnknownAsset):
	MAGIC = 0xF777E4A8

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "AnimSet/PerformanceSet {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class Texture(UnknownAsset):
	MAGIC = 0x5C4580B9

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "Texture {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class Cinematic2(UnknownAsset):
	MAGIC = 0xC4999B32

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "Cinematic2 {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class MaterialGraph(UnknownAsset):
	MAGIC = 0x07DC03E3

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "MaterialGraph {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class Level(UnknownAsset):
	MAGIC = 0x2AFE7495

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "Level {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class Zone(UnknownAsset):
	MAGIC = 0x8A0B1487

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "Zone {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class Conduit(UnknownAsset):
	MAGIC = 0x23A93984

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "Conduit {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class Localization(UnknownAsset):
	MAGIC = 0x122BB0AB

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "Localization {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class WwiseLookup(UnknownAsset):
	MAGIC = 0x35C9D886

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "WwiseLookup {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)

class VisualEffect(UnknownAsset):
	MAGIC = 0xF05EF819

	def __init__(self, f):
		UnknownAsset.__init__(self, f)

	def print_info(self, config):
		print "-------"
		print "VisualEffect {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print "size: {}".format(self.likely_is_dat1_size)
		print "-------"
		print ""

		self.dat1.print_info(config)
