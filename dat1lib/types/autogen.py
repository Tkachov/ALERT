import dat1lib.types.dat1
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class Actor(object):
	MAGIC = 0x7C207220

	def __init__(self, f):
		# MSMR
		# 5167 occurrences
		# size = 292..58644 (avg = 2782.3)
		# from 2 to 5 sections (avg = 4.4)
		#
		# examples: 815ECA36897F2155 (min size), B93103E693B0C988 (max size), 80029DC4DB44B189 (5 sections)

		# MM
		# 3793 occurrences
		# size = 292..51124 (avg = 2813.7)
		# from 2 to 5 sections (avg = 4.3)
		#
		# examples: 815ECA36897F2155 (min size), BAAE788E4A9CE960 (max size), 80045C4EB4D036F7 (5 sections)
		
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
		# MSMR
		# 101563 occurrences
		# size = 68..16687476 (avg = 11246.1)
		# from 0 to 13 sections (avg = 4.8)
		#
		# examples: 908967720123FAEC (min size), 975FE295868E3A97 (max size), 801C7AD11F80C415 (13 sections)

		# MM
		# 63110 occurrences
		# size = 68..11306980 (avg = 16570.8)
		# from 0 to 13 sections (avg = 5.5)
		#
		# examples: 803E59F5447F9A88 (min size), 9F2D52FB01A4D401 (max size), 80114FA50C1ED5A7 (13 sections)
		
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
		# MSMR
		# 1683 occurrences
		# size = 108..493940 (avg = 9808.5)
		# from 1 to 10 sections (avg = 4.5)
		#
		# examples: 9903DC1E58C18E58 (min size), A18BCEC8189C4022 (max size), 8067E77AEFE21A1C (10 sections)

		# MM
		# 953 occurrences
		# size = 108..863916 (avg = 19046.4)
		# from 1 to 10 sections (avg = 5.4)
		#
		# examples: A8F458FA46F0B8C8 (min size), 829740303741E942 (max size), 80CC4C76B08BAFE9 (10 sections)
		
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
		# MSMR
		# 724 occurrences
		# size = 2572..32168692 (avg = 1028002.4)
		# from 18 to 28 sections (avg = 23.0)
		#
		# examples: 9FD15C7DAB010DFD (min size), A0D237BF807F8B9F (max size), 8079C2A3952F3D9F (18 sections), 83FBD71137D3F6A8 (28 sections)

		# MM
		# 487 occurrences
		# size = 2940..20450284 (avg = 736747.4)
		# from 18 to 28 sections (avg = 22.2)
		#
		# examples: A6FE6EDA00BDC0CF (min size), 868F0E1B33099EDF (max size), 80186B0F3760E0B8 (18 sections), 840883A8DF616BE9 (28 sections)
		
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
		# MSMR
		# 1234 occurrences
		# size = 204..613540 (avg = 16019.3)
		# from 1 to 2 sections (avg = 1.5)
		#
		# examples: 93D2FB47CF888B46 (min size), AF207C743E768578 (max size), 800DFA948B7A05C6 (1 sections), 80010AD8DE1789A4 (2 sections)

		# MM
		# 1119 occurrences
		# size = 204..1035892 (avg = 21406.5)
		# from 1 to 2 sections (avg = 1.5)
		#
		# examples: 80372B922DE76D8F (min size), AF207C743E768578 (max size), 8004EB3B6A850706 (1 sections), 80010AD8DE1789A4 (2 sections)
		
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
		# MSMR
		# 1 occurrences
		# size = 17945492
		# always 15 sections
		#
		# examples: 93243FC0D3FE0498

		# MM
		# 1 occurrences
		# size = 14963868
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
		# MSMR
		# 5 occurrences
		# size = 164
		# always 2 sections
		#
		# examples: 83F4B7E7E9672F27

		# MM
		# 4 occurrences
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
		# MSMR
		# 23 occurrences
		# size = 5650545..7514348 (avg = 6015692.5)
		# always 9 sections
		#
		# examples: BE55D94F171BF8DE (min size), BE55D94F171BF8DE (max size)

		# MM
		# 32 occurrences
		# size = 1704117..4373349 (avg = 3123731.8)
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
		# MSMR
		# 1049 occurrences
		# size = 181300..1038404 (avg = 463254.6)
		# from 3 to 9 sections (avg = 5.9)
		#
		# examples: A8FE8763415A6F99 (min size), BEFDDF40CBCC9FC4 (max size), 835E7C81247705C0 (3 sections), 94437BF7006F34BB (9 sections)

		# MM: none
		
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

class MaterialGraph2(MaterialGraph):
	MAGIC = 0xFF60342A

	# MSMR: none

	# MM
	# 1157 occurrences
	# size = 185716..1237492 (avg = 468529.8)
	# from 3 to 9 sections (avg = 5.8)
	#
	# examples: 98E9BDEDDD2E0E39 (min size), 90EDE8261645D3FC (max size), 85ABB22196FFE129 (3 sections), 94437BF7006F34BB (9 sections)

#

class NodeGraphSection(dat1lib.types.sections.SerializedSection):
	TAG = -1
	TYPE = 'NodeGraph'

	def __init__(self, tag, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)
		self.tag = tag

	def get_short_suffix(self):
		return "type"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Node         |".format(self.tag))
		print(json.dumps(self.root, indent=4, sort_keys=True))
		if len(self.extras) > 0:
			print(" "*10, self.extras)

	def web_repr(self):
		return {"name": "Node {:08X}".format(self.tag), "type": "json", "readonly": True, "content": self.root}

class NodeGraph(object):
	MAGIC = 0x9E4E9BA4

	def __init__(self, f):
		# MSMR: none
		
		# MM
		# 101 occurrences
		# size = 3764..9728580 (avg = 295413.5)
		# from 7 to 5686 sections (avg = 170.0)
		#
		# examples: 91957ED40A4813B3 (min size), BF53FB9507F5A7B0 (max size)
		
		self.magic, self.size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print("[!] Bad NodeGraph magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

		for i in range(len(self.dat1.header.sections)):
			self.dat1.sections[i] = NodeGraphSection(self.dat1.header.sections[i].tag, self.dat1._sections_data[i], self.dat1)

	def save(self, f):
		self.size = self.dat1.header.size

		f.write(struct.pack("<II", self.magic, self.size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print("-------")
		print("NodeGraph {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("size: {}".format(self.size))
		print("-------")
		print()

		self.dat1.print_info(config)

#

class Texture(object):
	MAGIC = 0x5C4580B9

	def __init__(self, f):
		# MSMR
		# 25602 occurrences
		# size = 132..57372800 (avg = 266886.3)
		# always 1 sections
		#
		# examples: 95D6156483FC4B2E (min size), 8A59F83B570B11AC (max size), 800035F1EBDCBCEC

		# MM
		# 20652 occurrences
		# size = 132..59378816 (avg = 240317.9)
		# always 1 sections
		#
		# examples: 9894EC8A3A6A89FC (min size), B37E3F0781D14BAE (max size), 800035F1EBDCBCEC
		
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
		# MSMR
		# 4957 occurrences
		# size = 356..53212 (avg = 7198.9)
		# from 4 to 9 sections (avg = 7.0)
		#
		# examples: 80C19AB25B853A3D (min size), 8861893C5DCB68E1 (max size), 807C65DB74F19326 (4 sections), 817595E5CA5E1FDD (9 sections)

		# MM
		# 4215 occurrences
		# size = 356..550584 (avg = 10107.9)
		# from 4 to 10 sections (avg = 7.1)
		#
		# examples: 80C19AB25B853A3D (min size), BBA6299F7845D15A (max size), 807C65DB74F19326 (4 sections), 85570C67E0242FC3 (10 sections)
		
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
		# MSMR
		# 1 occurrences
		# size = 3502836
		# always 3 sections
		#
		# examples: A81AB0A616889CC2

		# MM
		# 1 occurrences
		# size = 2412580
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
		# MSMR
		# 12274 occurrences
		# size = 136..25607920 (avg = 563298.3)
		# from 1 to 39 sections (avg = 10.5)
		#
		# examples: 8024B53A94D71770 (min size), 801782CA955BA5D1 (max size), 9E68ECCCCCA82FCF (39 sections)

		# MM
		# 10473 occurrences
		# size = 136..27981124 (avg = 590531.8)
		# from 1 to 38 sections (avg = 9.3)
		#
		# examples: 801D9410B83924DD (min size), 833B331992AB0DCE (max size), 869F7D047B334435 (38 sections)
		
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
