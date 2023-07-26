import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.dat1
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

# common with .cinematic2

class x212BD372_Section(dat1lib.types.sections.Section):
	TAG = 0x212BD372
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2174 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24..28416 (avg = 678.9)
		#
		# examples: 80B6332B78CB1955 (min size), 903533D7C4E45412 (max size)

		# MM
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24..23640 (avg = 823.3)
		#
		# examples: 8066767AB8665577 (min size), BA773355A0CA1F3E (max size)

		self.count1, self.count2 = struct.unpack("<HH", data[:4])

		off = 4
		ENTRY_SIZE = 4
		count = self.count1
		self.values1 = [struct.unpack("<I", data[off + i*ENTRY_SIZE:off + (i+1)*ENTRY_SIZE])[0] for i in range(count)]
		off += count*ENTRY_SIZE

		self.unk1, self.unk2 = struct.unpack("<HH", data[off:off+4])
		off += 4

		# TODO: see 9B7700EBBC24E3AF, this part is 4 bytes off there
		
		count = self.count2
		self.hashes = []
		for i in range(count):
			self.hashes += [struct.unpack("<Q", data[off:off+8])[0]]
			off += 8

		self.string_offsets = []
		for i in range(count):
			self.string_offsets += [struct.unpack("<I", data[off:off+4])[0]]
			off += 4

	def get_short_suffix(self):
		return "212BD372 ({}/{})".format(self.count1, self.count2)

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 212BD372     |".format(self.TAG))
		print("  {} {} {} {}".format(self.count1, self.count2, self.unk1, self.unk2))
		print()

		for i in range(self.count1):
			print("  - {:<3}  {:08X}".format(i, self.values1[i]))
		print()

		for i in range(self.count2):
			s = self._dat1._strings_map.get(self.string_offsets[i], None)
			print("  - {:<3}  {:016X} {}".format(i, self.hashes[i], s))
		print()

#

class AnimSetBuiltSection(dat1lib.types.sections.Section):
	TAG = 0x6C69A660 # Anim Set Built
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2407 occurrences in 2407 files (always present)
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24
		#
		# examples: 8001A078B458EE04

		# MM
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24
		#
		# examples: 80186B0F3760E0B8
		
		ENTRY_SIZE = 2
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<h", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<h", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Anim Set Built ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Set Built    | {:6} values".format(self.TAG, len(self.entries)))
		print(self.entries)
		print("")

#

class AnimDriverClassBuiltSection(dat1lib.types.sections.Section):
	TAG = 0x66CA6C6F # Anim Driver Class built
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 1207 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 80..216000 (avg = 5557.7)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)

		# MM
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 80..156400 (avg = 3937.9)
		#
		# examples: 8019E233758A1721 (min size), B6C2891A5C7B1E0E (max size)
		
		ENTRY_SIZE = 80
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<" + "I"*14 + "f"*4 + "I"*2, data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Anim Driver Class built ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Class Built  | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			# (3971249573, 4, 0, 96, 0, 1, 0, 0, 0, 0, 0, 0, 0, 20, 1048576000, 1048576000, 1048576000, 1048576000, 191, 0)
			# (2049150217, 3, 4, 96, 0, 1, 0, 0, 0, 0, 0, 0, 0, 44, 1048576000, 1048576000, 1048576000, 1048576000, 187, 0)
			# (3449407077, 5, 4, 96, 0, 1, 0, 0, 0, 0, 0, 0, 0, 60, 1048576000, 1048576000, 1048576000, 1048576000, 195, 0)
			# sorted by tag
			tag,     a, b, always96, c, d, _, _, _, _, _, _, _, pos, float_r, float_g, float_b, float_a, e, f = x
			print("  - {:<3}  {:08X} {}".format(i, tag, self._dat1.get_string(pos + self._dat1.header.get_offset())))
			print("         {:<2} {:<3} {:<4} {:<4} {:<3} {:<4} {:<1} | {} {} {} {}".format(a, b, always96, c, d, e, f, float_r, float_g, float_b, float_a))
			print()

#

class AnimClipLookupSection(dat1lib.types.sections.Section):
	TAG = 0xB79CF1D7 # Anim Clip Lookup
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2175 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24..64872 (avg = 1603.3)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)

		# MM
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24..50064 (avg = 1783.3)
		#
		# examples: 8019E233758A1721 (min size), BA773355A0CA1F3E (max size)
		
		ENTRY_SIZE = 24
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<IIiQI", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]
		# e[0] is used as e[12] in 0x73CEE17F, if e[1] == 0
		# e[0] is unknown if e[1] == 32768
		# e[2] == -1
		# e[3] is from 0x212BD372 values[]; .animclip asset ids (not present in 0xC8CE8D96) if e[1] == 0, unknown otherwise (e[1] == 256)
		# e[4] == 0

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Anim Clip Lookup ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Clip Lookup  | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			print("  - {:<3}  {:08X} {:5} {} {:016X} {}".format(i, *x))
		print("")

#

class AnimDriverClassDataSection(dat1lib.types.sections.Section):
	TAG = 0x73CEE17F # Anim Driver Class data
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 1204 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 96..259200 (avg = 7666.1)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)

		# MM
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 96..393456 (avg = 7027.5)
		#
		# examples: 8019E233758A1721 (min size), 829740303741E942 (max size)

		# seems to be related to 0xA40B51D2
		
		ENTRY_SIZE = 96
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<Ihh" + 'f'*9 + "I" + 'f'*11 + 'hh', data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Anim Driver Class data ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Class data   | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			print("  - {:<3}  {:08X}  {:3} {:3}  {:08X}".format(i, x[0], x[1], x[2], x[12]))
			# print("         {}".format(x))
		print("")
#

class AnimDriverClassLookupSection(dat1lib.types.sections.Section):
	TAG = 0xA40B51D2 # Anim Driver Class lookup
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 1207 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 16..43200 (avg = 1111.5)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)

		# MM
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 16..31280 (avg = 787.5)
		#
		# examples: 8019E233758A1721 (min size), B6C2891A5C7B1E0E (max size)

		# seems to be related to 0x73CEE17F (0xA40B51D2's entry[0] == offset of entry in 0x73CEE17F -- which isn't hard tho since it's 96*index)
		# but, based on occurrences amount, they are not necessarily going together
		
		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<IIII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Anim Driver Class lookup ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Class Lookup | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			print("  - {:<3}  {}".format(i, x))
		print("")

#

class AnimClipDataSection(dat1lib.types.sections.Section):
	TAG = 0x9FD19C20 # Anim Clip Data
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 783 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 80..29793232 (avg = 829093.4)
		#
		# examples: 9D2A0B2B472ADED0 (min size), A0D237BF807F8B9F (max size)

		# MM
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 80..19315664 (avg = 633274.9)
		#
		# examples: 90362EE3DA39CC6C (min size), 868F0E1B33099EDF (max size)
		
		self.version = self._dat1.version
		self.inner_dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(data), self, ignore_sections_exceptions=True)

	def get_short_suffix(self):
		return "Anim Clip Data -- inner dat1 ({} bytes, {} sections)".format(len(self._raw), len(self.inner_dat1.sections))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Clip Data    | {:6} bytes -- inner DAT1".format(self.TAG, len(self._raw)))

		print("=" * 40)
		self.inner_dat1.print_info(config)
		print("=" * 40)
