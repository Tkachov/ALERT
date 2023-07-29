import dat1lib.crc64 as crc64
import dat1lib.types.sections
import io
import struct

class InnerAssetsContainerSection(dat1lib.types.sections.Section):
	TAG = 0x4D7BC1C7
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 6099 occurrences in 12274 files
		# size = 40..3762252 (avg = 81807.8)
		#
		# examples: 8151F22E4A189346 (min size), 9419A66DCDCE388E (max size)

		# MM
		# 4950 occurrences in 10473 files
		# size = 40..3796588 (avg = 69305.3)
		#
		# examples: 8035E8D12E1FE889 (min size), 9419A66DCDCE388E (max size)

		# RCRA
		# 65 occurrences in 9046 files
		# size = 60..421320 (avg = 27864.3)
		#
		# examples: 8539C9C98977EE46 (min size), 8683FD7F7ABDC494 (max size)

		self.entries = []

		i = 0
		while i < len(data):
			magic, size = struct.unpack("<II", data[i:i+8])
			i += 8
			self.entries += [(magic, size, data[i:i+size])]
			i += size

	def get_short_suffix(self):
		return "inner assets ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Inner Assets | {:6} assets".format(self.TAG, len(self.entries)))

		for i, e in enumerate(self.entries):
			print("- {:<2}  {:08X}  {} bytes".format(i, e[0], e[1]))
			print("       {:08X}  {} sections".format(struct.unpack("<I", e[2][4:8])[0], struct.unpack("<I", e[2][12:16])[0]))
			print()

###

class ZoneReferencesSection(dat1lib.types.sections.ReferencesSection):
	TAG = 0x91DE11D9
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.ReferencesSection.__init__(self, data, container)

		# MSMR
		# 1248 occurrences in 12274 files
		# size = 16..12624 (avg = 1178.2)
		#
		# examples: 8087A66DB8F99689 (min size), 974EB47F6B2CA8E3 (max size)

		# MM
		# 1044 occurrences in 10473 files
		# size = 16..12240 (avg = 1393.1)
		#
		# examples: 8060F01DB1EFC3AB (min size), 974EB47F6B2CA8E3 (max size)

		# RCRA
		# 335 occurrences in 9046 files
		# size = 16..11680 (avg = 782.6)
		#
		# examples: 85D841EBD01D04FC (min size), B234D5DB373273D5 (max size)

	def get_short_suffix(self):
		return "Zone References ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Zone Refs    | {:6} entries".format(self.TAG, len(self.entries)))
		dat1lib.types.sections.ReferencesSection.print_verbose(self, config)
		print("    string offsets =", [x[1] for x in self.entries])
		print()

###

class ZoneMaterialOverridesSection(dat1lib.types.sections.Section):
	TAG = 0xE4158AC3 # "Zone Material Overrides"
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2167 occurrences in 12274 files
		# size = 16..17712 (avg = 1028.3)
		#
		# examples: 8015FB3B80A9AD40 (min size), A050B40CE45C5AFD (max size)

		# MM
		# 1960 occurrences in 10473 files
		# size = 16..13216 (avg = 1258.9)
		#
		# examples: 8007054377A3EA0F (min size), 869F7D047B334435 (max size)

		# RCRA
		# 882 occurrences in 9046 files
		# size = 16..10192 (avg = 286.1)
		#
		# examples: 805224F2BED38913 (min size), BB7D7B266225CF80 (max size)
		
		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<IIQ", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<IIQ", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Zone Material Overrides ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Mat. Ovrrids | {:6} entries".format(self.TAG, len(self.entries)))

		for i, x in enumerate(self.entries):
			print("  - {:<2}  {:016X}  {:08X}  {:08X}".format(i, x[2], x[1], x[0]))
		print("")
