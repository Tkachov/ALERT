import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class Soundbank(object):
	MAGIC = 0x7E4F1BB7

	def __init__(self, f, version=None):
		# MSMR
		# 1345 occurrences
		# size = 260..29288741 (avg = 773143.8)
		# from 3 to 4 sections (avg = 3.9)
		#
		# examples: 8C129CA7DA42BEAE (min size), 9B3473B5F2EF53D3 (max size), 803894E1B9984FE9 (3 sections), 801825F7A321A714 (4 sections)

		# MM
		# 1239 occurrences
		# size = 244..22520715 (avg = 522419.3)
		# from 3 to 4 sections (avg = 3.9)
		#
		# examples: 8208A29C47736EAD (min size), 9B3473B5F2EF53D3 (max size), 800BAAC604A8B370 (4 sections)

		self.version = version
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Soundbank magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Soundbank {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("    size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

class SoundbankRcra(Soundbank):
	MAGIC = 0xC2841216

	# RCRA
	# 1218 occurrences
	# size = 208..115413669 (avg = 930100.1)
	# from 3 to 4 sections (avg = 3.9)
	#
	# examples: 80401892FB7E19F8 (min size), 80E6D1589338AECF (max size), 800582AB4AE61DB1 (4 sections)

class Soundbank2(Soundbank):
	MAGIC = 0xD61E269F
