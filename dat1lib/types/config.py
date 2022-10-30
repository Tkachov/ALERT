import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class Config(object):
	MAGIC = 0x21A56F68
	EMPTY_DATA = struct.pack("<II", 0x21A56F68, len(dat1lib.types.dat1.DAT1.EMPTY_DATA)) + b'\0'*28 + dat1lib.types.dat1.DAT1.EMPTY_DATA

	def __init__(self, f):
		# 2521 occurrences
		# size = 180..1239920 (avg = 4610.3)
		# from 2 to 3 sections (avg = 2.5)
		#
		# examples: 813381135A2CC078 (min size), A5C3BBB75C76D0FA (max size), 800C715445D02494 (2 sections), 8008619CBD504B56 (3 sections)
		
		self.magic, self.dat1_size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Config magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

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
		print("-------")
		print("Config {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("- size   = {}".format(self.dat1_size))
		print("-------")
		print("")

		self.dat1.print_info(config)
