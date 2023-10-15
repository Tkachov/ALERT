import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

# Sunset Overdrive PC (aka i16) sections

class Actor_I16(object):
	MAGIC = 0x5AB80409

	def __init__(self, f, version=None):
		# 2568 occurrences
		# size = 130..6423 (avg = 895.7)
		# from 2 to 5 sections (avg = 4.6)
		#
		# examples: 140C7175 (min size), F0C5BEFF (max size), 006C6ED7 (5 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Actor_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Actor_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class AnimSetPerformanceSet_I16(object):
	MAGIC = 0xDC69CE74

	def __init__(self, f, version=None):
		# 901 occurrences
		# size = 99..28959219 (avg = 268299.1)
		# from 1 to 8 sections (avg = 4.2)
		#
		# examples: 0D3F10BF (min size), EA60260B (max size), 03DF42A5 (8 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad AnimSetPerformanceSet_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("AnimSetPerformanceSet_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Atmosphere_I16(object):
	MAGIC = 0x8539E081

	def __init__(self, f, version=None):
		# 16 occurrences
		# size = 1875400..2033140 (avg = 1912266.2)
		# always 2 sections
		#
		# examples: 5542571A (min size), 30846F2B (max size), 00B27A40

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Atmosphere_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Atmosphere_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Cinematic_I16(object):
	MAGIC = 0xE92467FE

	def __init__(self, f, version=None):
		# 2 occurrences
		# size = 713..1881 (avg = 1297.0)
		# always 2 sections
		#
		# examples: 34C9DD49 (min size), 15625880 (max size)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Cinematic_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Cinematic_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Cinematic2_I16(object):
	MAGIC = 0x5A5FA996

	def __init__(self, f, version=None):
		# 350 occurrences
		# size = 1096..15188731 (avg = 789879.3)
		# from 13 to 17 sections (avg = 16.1)
		#
		# examples: 3CAAA304 (min size), A563E049 (max size), 191E68EF (13 sections), 01032961 (17 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Cinematic2_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Cinematic2_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class ConduitConfig_I16(object):
	MAGIC = 0x1EE23F76

	def __init__(self, f, version=None):
		# 3415 occurrences
		# size = 164..84245 (avg = 1583.6)
		# from 1 to 3 sections (avg = 2.3)
		#
		# examples: 81B5EE07 (min size), 88E8D092 (max size), 00226F29 (1 sections), 004CD30B (3 sections)

		# TODO: derive from Config?
		# TODO: research how .conduit differs from .config

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad ConduitConfig_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("ConduitConfig_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Level_I16(object):
	MAGIC = 0x6FEE7FE8

	def __init__(self, f, version=None):
		# 1 occurrence
		# size = 400054
		# always 11 sections
		#
		# examples: 34ABC921

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Level_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Level_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class LightGrid_I16(object):
	MAGIC = 0xFB11963F

	def __init__(self, f, version=None):
		# 46816 occurrences
		# size = 494..74168 (avg = 24577.0)
		# from 1 to 2 sections (avg = 1.8)
		#
		# examples: 000EE322 (min size), 251A256A (max size), 00011946 (2 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad LightGrid_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("LightGrid_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Localization_I16(object):
	MAGIC = 0x1A92855A

	def __init__(self, f, version=None):
		# 19 occurrences
		# size = 131..2194602 (avg = 1652353.0)
		# always 1 sections
		#
		# examples: 2F0C877C (min size), 2F0C877C (max size)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Localization_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Localization_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Material_I16(object):
	MAGIC = 0xBDC826B8

	def __init__(self, f, version=None):
		# 6925 occurrences
		# size = 155..1801 (avg = 593.8)
		# from 1 to 5 sections (avg = 4.5)
		#
		# examples: 7824FB32 (min size), 6254DEE0 (max size), 0205FDFF (1 sections), 000C8FCD (5 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Material_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Material_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class MaterialGraph_I16(object):
	MAGIC = 0xE79C1DD5

	def __init__(self, f, version=None):
		# 1012 occurrences
		# size = 8728..46118 (avg = 23997.9)
		# from 3 to 7 sections (avg = 5.6)
		#
		# examples: 1E2A8F51 (min size), 6A931013 (max size), 09EA8F00 (3 sections), 7376D96B (7 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad MaterialGraph_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("MaterialGraph_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Model_I16(object):
	MAGIC = 0x6AE15C79

	def __init__(self, f, version=None):
		# 8780 occurrences
		# size = 348..7477156 (avg = 138959.3)
		# from 2 to 24 sections (avg = 13.4)
		#
		# examples: AE31F0D5 (min size), 14741BE4 (max size), 0395209B (24 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Model_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Model_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class ModelVariant_I16(object):
	MAGIC = 0x9F120E73

	def __init__(self, f, version=None):
		# 2 occurrences
		# size = 9693..9779 (avg = 9736.0)
		# always 2 sections
		#
		# examples: 915165CD (min size), 06703DB9 (max size)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad ModelVariant_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("ModelVariant_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Texture_I16(object):
	MAGIC = 0x61F99799

	def __init__(self, f, version=None):
		# 42840 occurrences
		# size = 108..3339790 (avg = 116673.5)
		# always 1 section
		#
		# examples: 2DD2951E (min size), AB6FF0D2 (max size), 0001E8B9

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Texture_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Texture_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Soundbank_I16(object):
	MAGIC = 0xB38AE498

	def __init__(self, f, version=None):
		# 1473 occurrences
		# size = 194..19837245 (avg = 318160.7)
		# from 3 to 4 sections (avg = 3.9)
		#
		# examples: AEA94DA2 (min size), 5264EACE (max size), 059C67FD (3 sections), 010FB3C2 (4 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Soundbank_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Soundbank_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class VisualEffect_I16(object):
	MAGIC = 0x00D54C81

	def __init__(self, f, version=None):
		# 2348 occurrences
		# size = 337..6346 (avg = 1329.4)
		# from 4 to 9 sections (avg = 5.9)
		#
		# examples: B7313548 (min size), 4DB5928D (max size), 011D25F5 (4 sections), 327F8C96 (9 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad VisualEffect_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("VisualEffect_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Zone_I16(object):
	MAGIC = 0xD79E37F9

	def __init__(self, f, version=None):
		# 4936 occurrences
		# size = 67..24081757 (avg = 35187.7)
		# from 0 to 25 sections (avg = 5.7)
		#
		# examples: 003E6582 (min size), 2CE51F8A (max size), 45E6A363 (25 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad Zone_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("Zone_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class ZonePhysics_I16(object):
	MAGIC = 0xE6E36BF0

	def __init__(self, f, version=None):
		# 1112 occurrences
		# size = 83..1544901 (avg = 123677.7)
		# from 0 to 1 sections (avg = 0.8)
		#
		# examples: 036306A5 (min size), 78B6B07E (max size), 0023484A (1 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad ZonePhysics_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("ZonePhysics_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class ZoneStatic_I16(object):
	MAGIC = 0xBA452850

	def __init__(self, f, version=None):
		# 419 occurrences
		# size = 123..1551312 (avg = 129696.9)
		# from 1 to 2 sections (avg = 1.9)
		#
		# examples: 05587038 (min size), 5687A013 (max size), 0012CD7C (2 sections)

		self.version = version
		if version is None:
			self.version = dat1lib.VERSION_SO
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad ZoneStatic_I16 magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("ZoneStatic_I16 {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)
