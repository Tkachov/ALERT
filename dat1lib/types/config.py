import dat1lib.types.dat1
import dat1lib.types.sections.config.references
import dat1lib.types.sections.config.serialized
import dat1lib.utils as utils
import io
import struct

class Config(object):
	MAGIC = 0x21A56F68
	EMPTY_DATA = struct.pack("<II", 0x21A56F68, len(dat1lib.types.dat1.DAT1.EMPTY_DATA)) + b'\0'*28 + dat1lib.types.dat1.DAT1.EMPTY_DATA

	def __init__(self, f, version=None):
		# MSMR
		# 2521 occurrences
		# size = 180..1239920 (avg = 4610.3)
		# from 2 to 3 sections (avg = 2.5)
		#
		# examples: 813381135A2CC078 (min size), A5C3BBB75C76D0FA (max size), 800C715445D02494 (2 sections), 8008619CBD504B56 (3 sections)

		# MM
		# 2026 occurrences
		# size = 180..1578624 (avg = 5255.9)
		# from 2 to 3 sections (avg = 2.4)
		#
		# examples: 813381135A2CC078 (min size), 97425517EBC3BB3F (max size), 80021D6AAE50A75C (2 sections), 80419E87ECF4E626 (3 sections)

		self.version = version
		
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

	#

	def get_type_section(self):
		return self.dat1.get_section(dat1lib.types.sections.config.serialized.ConfigTypeSection.TAG)

	def get_content_section(self):
		return self.dat1.get_section(dat1lib.types.sections.config.serialized.ConfigContentSection.TAG)

	def get_references_section(self):
		return self.dat1.get_section(dat1lib.types.sections.config.references.ReferencesSection.TAG)

	#

	def print_info(self, config):
		print("-------")
		print("Config {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("- size   = {}".format(self.dat1_size))
		print("-------")
		print("")

		self.dat1.print_info(config)

class ConfigRcra(Config):
	MAGIC = 0x21A56F68

	# RCRA
	# 1847 occurrences
	# size = 144..4320644 (avg = 6285.8)
	# from 2 to 3 sections (avg = 2.3)
	#
	# examples: 94982925AD887B35 (min size), BB876CAC4C37B181 (max size), 80483C8A48424009 (2 sections), 8001C43CEBA5E2FA (3 sections)
