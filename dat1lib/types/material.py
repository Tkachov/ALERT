import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class Material(object):
	MAGIC = 0x1C04EF8C

	def __init__(self, f):
		# 13178 occurrences
		# size = 260..1092164 (avg = 149987.8)
		# from 2 to 12 sections (avg = 4.1)
		#
		# examples: 8B5BEC7D10F0F5D6 (min size), 8E1F4B600684B170 (max size), 8000B10F551366C6 (2 sections), 80558F950ED7ADEE (12 sections)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Material magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Material {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)
