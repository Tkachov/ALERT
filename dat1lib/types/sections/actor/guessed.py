import dat1lib.crc64 as crc64
import dat1lib.types.sections
import io
import struct

class ActorModelNameSection(dat1lib.types.sections.Section):
	TAG = 0x32FAC8E0
	TYPE = 'Actor'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 5167 occurrences in 5167 files (always present)
		# size = 4
		# always first
		#
		# examples: 80029DC4DB44B189

		# MM
		# 3793 occurrences in 3793 files (always present)
		# size = 4
		# always first
		#
		# examples: 80027411351D35BA
		
		self.value = struct.unpack("<I", data)[0]

	def save(self):
		return struct.pack("<I", self.value)

	def get_short_suffix(self):
		return "model name"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Model Name   | {}".format(self.TAG, self._dat1.get_string(self.value)))

###

class ActorAssetRefsSection(dat1lib.types.sections.ReferencesSection):
	TAG = 0x3AB204B9 # Actor Asset Refs
	TYPE = 'Actor'

	def __init__(self, data, container):
		dat1lib.types.sections.ReferencesSection.__init__(self, data, container)

		# MSMR
		# 4928 occurrences in 5167 files
		# size = 16..2336 (avg = 101.9)
		#
		# examples: 8012CEC29FE92381 (min size), BAAE788E4A9CE960 (max size)

		# MM
		# 3595 occurrences in 3793 files
		# size = 16..2336 (avg = 101.6)
		#
		# examples: 80027411351D35BA (min size), BAAE788E4A9CE960 (max size)

	def get_short_suffix(self):
		return "Actor Asset Refs ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Asset Refs   | {:6} entries".format(self.TAG, len(self.entries)))
		dat1lib.types.sections.ReferencesSection.print_verbose(self, config)

###

class ComponentDefinitionsSection(dat1lib.types.sections.Section):
	TAG = 0x135832C8
	TYPE = 'Actor'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 4301 occurrences in 5167 files
		# size = 32..1056 (avg = 115.8)
		#
		# examples: 8012CEC29FE92381 (min size), 88EBA704687556DC (max size)

		# MM
		# 2993 occurrences in 3793 files
		# size = 32..800 (avg = 109.9)
		#
		# examples: 8014A0707A32D982 (min size), B62EBBE477CDF302 (max size)
		
		ENTRY_SIZE = 32
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<IIIIIIII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<IIIIIIII", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "components defs ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Comp. Defs   | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			s = self._dat1.get_string(x[2])
			h = crc64.hash(s)
			print("")
			print("  - {:<3}  {}".format(i, s))
			print("         {:08X} {:08X} {:08X}".format(x[0], x[1], x[3]))
			print("         0={}, offset={}, size={}, 0={}".format(x[4], x[5], x[6], x[7]))
		print("")

###

class ComponentsDataSection(dat1lib.types.sections.Section):
	TAG = 0x6D4301EF
	TYPE = 'Actor'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 3506 occurrences in 5167 files
		# size = 32..30224 (avg = 1711.7)
		#
		# examples: 8074615B5D3B13A8 (min size), B93103E693B0C988 (max size)

		# MM
		# 2461 occurrences in 3793 files
		# size = 32..26240 (avg = 1795.5)
		#
		# examples: 81C1F02C8DB374A9 (min size), BAAE788E4A9CE960 (max size)

		# has strings in it

		this_section_real_offset = 0
		for s in container.header.sections:
			if s.tag == self.TAG:
				this_section_real_offset = s.offset
				break

		self.entries = []

		headers = container.get_section(ComponentDefinitionsSection.TAG)
		for e in headers.entries:
			try:
				offset, size = e[5], e[6]
				offset -= this_section_real_offset

				a, b, c, data_len = struct.unpack("<IIII", data[offset:offset+16])
				comp_data = data[offset+16:offset+size]

				if data_len != size-16:
					print("[!] size={}, data_len={}, expected data_len={}".format(size, data_len, size-16))

				self.entries += [(a, b, c, data_len, comp_data)]
			except:
				pass

	def get_short_suffix(self):
		return "components data ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Comp. Data   | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			a, b, c, data_len, comp_data = x
			print("  - {:<3}  {:08X} {:08X} {:08X}".format(i, a, b, c))
		print("")

