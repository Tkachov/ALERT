import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class Atmosphere(object):
	MAGIC = 0x39F27E27

	def __init__(self, f, version=None):
		# MSMR
		# 133 occurrences
		# size = 1676..2770800 (avg = 1588694.2)
		# from 1 to 4 sections (avg = 3.3)
		#
		# examples: 970D43801CB614DC (min size), B11F882525900C32 (max size), 80BA05E01E62AE5B (4 sections)

		# MM
		# 108 occurrences
		# size = 1685..2770752 (avg = 1067797.4)
		# from 2 to 4 sections (avg = 3.1)
		#
		# examples: 93D0C8E529805B2C (min size), 86CBB80173F9A1B8 (max size), 81B1736360576794 (2 sections), 80BA05E01E62AE5B (4 sections)

		self.version = version
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Atmosphere magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Atmosphere {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

class AtmosphereRcra(Atmosphere):
	MAGIC = 0x21D5E72C

	# RCRA
	# 95 occurrences
	# size = 1864..2771292 (avg = 816909.9)
	# from 1 to 4 sections (avg = 3.0)
	#
	# examples: A7F253C95A0A0098 (min size), B431B895EFE8E17D (max size), 837E5685BA7DF0F1 (4 sections)

class Atmosphere2(Atmosphere):
	MAGIC = 0x39835F68
