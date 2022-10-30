import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class Actor(object):
	MAGIC = 0x7C207220

	def __init__(self, f):
		# 5167 occurrences
		# size = 292..58644 (avg = 2782.3)
		# from 2 to 5 sections (avg = 4.4)
		#
		# examples: 815ECA36897F2155 (min size), B93103E693B0C988 (max size), 80029DC4DB44B189 (5 sections)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Actor magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Actor {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class AnimClip(object): # animclip/performanceclip
	MAGIC = 0xC96F58F3

	def __init__(self, f):
		# 101563 occurrences
		# size = 68..16687476 (avg = 11246.1)
		# from 0 to 13 sections (avg = 4.8)
		#
		# examples: 908967720123FAEC (min size), 975FE295868E3A97 (max size), 801C7AD11F80C415 (13 sections)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad AnimClip_PerformanceClip magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("AnimClip/PerformanceClip {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class AnimSet(object): # animset/performanceset
	MAGIC = 0xF777E4A8

	def __init__(self, f):
		# 1683 occurrences
		# size = 108..493940 (avg = 9808.5)
		# from 1 to 10 sections (avg = 4.5)
		#
		# examples: 9903DC1E58C18E58 (min size), A18BCEC8189C4022 (max size), 8067E77AEFE21A1C (10 sections)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad AnimSet_PerformanceSet magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("AnimSet/PerformanceSet {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class Cinematic2(object):
	MAGIC = 0xC4999B32

	def __init__(self, f):
		# 724 occurrences
		# size = 2572..32168692 (avg = 1028002.4)
		# from 18 to 28 sections (avg = 23.0)
		#
		# examples: 9FD15C7DAB010DFD (min size), A0D237BF807F8B9F (max size), 8079C2A3952F3D9F (18 sections), 83FBD71137D3F6A8 (28 sections)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Cinematic2 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Cinematic2 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class Conduit(object):
	MAGIC = 0x23A93984

	def __init__(self, f):
		# 1234 occurrences
		# size = 204..613540 (avg = 16019.3)
		# from 1 to 2 sections (avg = 1.5)
		#
		# examples: 93D2FB47CF888B46 (min size), AF207C743E768578 (max size), 800DFA948B7A05C6 (1 sections), 80010AD8DE1789A4 (2 sections)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Conduit magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Conduit {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class Level(object):
	MAGIC = 0x2AFE7495

	def __init__(self, f):
		# 1 occurrences
		# size = 17945492
		# always 15 sections
		#
		# examples: 93243FC0D3FE0498
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Level magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Level {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class LevelLight(object):
	MAGIC = 0x567CC2F0

	def __init__(self, f):
		# 5 occurrences
		# size = 164
		# always 2 sections
		#
		# examples: 83F4B7E7E9672F27
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad LevelLight magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("LevelLight {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)
#

class Localization(object):
	MAGIC = 0x122BB0AB

	def __init__(self, f):
		# 23 occurrences
		# size = 5650545..7514348 (avg = 6015692.5)
		# always 9 sections
		#
		# examples: BE55D94F171BF8DE (min size), BE55D94F171BF8DE (max size)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Localization magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Localization {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class MaterialGraph(object):
	MAGIC = 0x07DC03E3

	def __init__(self, f):
		# 1049 occurrences
		# size = 181300..1038404 (avg = 463254.6)
		# from 3 to 9 sections (avg = 5.9)
		#
		# examples: A8FE8763415A6F99 (min size), BEFDDF40CBCC9FC4 (max size), 835E7C81247705C0 (3 sections), 94437BF7006F34BB (9 sections)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad MaterialGraph magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("MaterialGraph {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class Texture(object):
	MAGIC = 0x5C4580B9

	def __init__(self, f):
		# 25602 occurrences
		# size = 132..57372800 (avg = 266886.3)
		# always 1 sections
		#
		# examples: 95D6156483FC4B2E (min size), 8A59F83B570B11AC (max size), 800035F1EBDCBCEC
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		# <magic> <dat1 size> <texture block size>
		# <zero> <zero> <texture block size>
		# <zero> <zero> <zero>

		if self.magic != self.MAGIC:
			print("[!] Bad Texture magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Texture {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class VisualEffect(object):
	MAGIC = 0xF05EF819

	def __init__(self, f):
		# 4957 occurrences
		# size = 356..53212 (avg = 7198.9)
		# from 4 to 9 sections (avg = 7.0)
		#
		# examples: 80C19AB25B853A3D (min size), 8861893C5DCB68E1 (max size), 807C65DB74F19326 (4 sections), 817595E5CA5E1FDD (9 sections)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad VisualEffect magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("VisualEffect {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class WwiseLookup(object):
	MAGIC = 0x35C9D886

	def __init__(self, f):
		# 1 occurrences
		# size = 3502836
		# always 3 sections
		#
		# examples: A81AB0A616889CC2
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad WwiseLookup magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("WwiseLookup {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)

#

class Zone(object):
	MAGIC = 0x8A0B1487

	def __init__(self, f):
		# 12274 occurrences
		# size = 136..25607920 (avg = 563298.3)
		# from 1 to 39 sections (avg = 10.5)
		#
		# examples: 8024B53A94D71770 (min size), 801782CA955BA5D1 (max size), 9E68ECCCCCA82FCF (39 sections)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		# <magic> <size of first dat1> <size of second dat1> <zeros...>

		if self.magic != self.MAGIC:
			print("[!] Bad Zone magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Zone {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print("")

		self.dat1.print_info(config)
