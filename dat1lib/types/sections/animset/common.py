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

		# 2174 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24..28416 (avg = 678.9)
		#
		# examples: 80B6332B78CB1955 (min size), 903533D7C4E45412 (max size)

		self.version, self.count = struct.unpack("<HH", data[:4])

		self.ab, self.c, self.d, self.unk2, self.count2, self.count3 = None, None, None, None, None, None
		off = 20
		if self.version == 1:
			off = 16
			self.ab, self.c, self.d, self.unk2 = struct.unpack("<IHHI", data[4:16])
		else:
			self.ab, = struct.unpack("<I", data[4:8]) # `unk1` times "<H"?
			self.c, self.d = struct.unpack("<HH", data[8:12])
			self.unk2, self.count2, self.count3 = struct.unpack("<IHH", data[12:20])

		cnt = self.count
		self.values = []
		for i in range(cnt):
			self.values += [struct.unpack("<Q", data[off:off+8])[0]]
			off += 8

		self.values2 = []
		if self.version == 1:
			rest = data[off:]
			ENTRY_SIZE = 4
			count = len(data)//ENTRY_SIZE
			self.values2 = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]
		else:
			for i in range(cnt):
				self.values2 += [struct.unpack("<I", data[off:off+4])[0]]
				off += 4		

	def get_short_suffix(self):
		return "212BD372 ({})".format(len(self.values))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 212BD372     | {:6} entries".format(self.TAG, len(self.values)))
		print("  {} {} {:08X} {} {} {:08X} {} {}".format(self.version, self.count, self.ab, self.c, self.d, self.unk2, self.count2, self.count3))
		if self.version == 1:
			for i in range(len(self.values)):
				print("  - {:<3}  {:016X}".format(i, self.values[i]))
			print(self.values2)
		else:
			for i in range(len(self.values)):
				print("  - {:<3}  {:016X} {}".format(i, self.values[i], self.values2[i]))
		print("")

#

class x6C69A660_Section(dat1lib.types.sections.Section):
	TAG = 0x6C69A660
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2407 occurrences in 2407 files (always present)
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24
		#
		# examples: 8001A078B458EE04
		
		ENTRY_SIZE = 2
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<h", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "6C69A660 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 6C69A660     | {:6} values".format(self.TAG, len(self.entries)))
		print(self.entries)
		print("")

#

class x66CA6C6F_Section(dat1lib.types.sections.Section):
	TAG = 0x66CA6C6F
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1207 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 80..216000 (avg = 5557.7)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)
		
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
		return "66CA6C6F ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 66CA6C6F     | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			# (3971249573, 4, 0, 96, 0, 1, 0, 0, 0, 0, 0, 0, 0, 20, 1048576000, 1048576000, 1048576000, 1048576000, 191, 0)
			# (2049150217, 3, 4, 96, 0, 1, 0, 0, 0, 0, 0, 0, 0, 44, 1048576000, 1048576000, 1048576000, 1048576000, 187, 0)
			# (3449407077, 5, 4, 96, 0, 1, 0, 0, 0, 0, 0, 0, 0, 60, 1048576000, 1048576000, 1048576000, 1048576000, 195, 0)
			# sorted by tag
			tag,     a, b, always96, c, d, _, _, _, _, _, _, _, pos, float_r, float_g, float_b, float_a, e, f = x
			print("  - {:<3}  {:08X} {:4} | {:2} {:3} {:4} {:4} {:3} {:4} {:1} | {} {} {} {}".format(i, tag, pos, a, b, always96, c, d, e, f, float_r, float_g, float_b, float_a))
		print("")

#

class xB79CF1D7_Section(dat1lib.types.sections.Section): # aka anim_clip_lookup
	TAG = 0xB79CF1D7
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2175 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 24..64872 (avg = 1603.3)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)
		
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
		return "B79CF1D7 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | B79CF1D7     | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			print("  - {:<3}  {:08X} {:5} {} {:016X} {}".format(i, *x))
		print("")

#

class x73CEE17F_Section(dat1lib.types.sections.Section):
	TAG = 0x73CEE17F
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1204 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 96..259200 (avg = 7666.1)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)

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
		return "73CEE17F ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 73CEE17F     | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			print("  - {:<3}  {:08X}  {:3} {:3}  {:08X}".format(i, x[0], x[1], x[2], x[12]))
			# print("         {}".format(x))
		print("")
#

class xA40B51D2_Section(dat1lib.types.sections.Section):
	TAG = 0xA40B51D2
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1207 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 16..43200 (avg = 1111.5)
		#
		# examples: 80176C7A46F8A544 (min size), B339513408DB6431 (max size)

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
		return "A40B51D2 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | A40B51D2     | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			print("  - {:<3}  {}".format(i, x))
		print("")

#

class x9FD19C20_Section(dat1lib.types.sections.Section): # aka anim_clip_data
	TAG = 0x9FD19C20
	TYPE = 'AnimSet/PerformanceSet/Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 783 occurrences in 2407 files
		# met in AnimSet/PerformanceSet, Cinematic2
		# size = 80..29793232 (avg = 829093.4)
		#
		# examples: 9D2A0B2B472ADED0 (min size), A0D237BF807F8B9F (max size)
		
		self.inner_dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(data), self)

	def get_short_suffix(self):
		return "inner dat1 ({} bytes, {} sections)".format(len(self._raw), len(self.inner_dat1.sections))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Inner DAT1   | {:6} bytes".format(self.TAG, len(self._raw)))

		print("=" * 40)
		self.inner_dat1.print_info(config)
		print("=" * 40)
