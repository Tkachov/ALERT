import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class xF5260180_Section(dat1lib.types.sections.Section):
	TAG = 0xF5260180
	TYPE = 'material'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 13170 occurrences in 13178 files
		# size = 48..3552 (avg = 450.7)
		#
		# examples: 8010653ABB4F13F1 (min size), 8D5EB677647A4385 (max size)

		self.data_size, self.unk1, self.unk2, self.unk3, self.unk4 = struct.unpack("<IIIII", data[:20])
		self.materials_count, self.unk5, self.unk6, self.unk7, self.unk8 = struct.unpack("<IIIII", data[20:40])

		self.unk9 = data[40:self.unk4]
		rest = data[self.unk4:]

		ENTRY_SIZE = 8
		count = self.materials_count
		self.materials = [struct.unpack("<II", rest[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

		self.strings = rest[self.materials_count*8:] # TODO: use dat1lib.types.sections.StringsSection here?

	def save(self):
		of = io.BytesIO(bytes())

		self.data_size = self.unk4 + self.materials_count * 8 + len(self.strings)

		of.write(struct.pack("<IIIII", self.data_size, self.unk1, self.unk2, self.unk3, self.unk4))
		of.write(struct.pack("<IIIII", self.materials_count, self.unk5, self.unk6, self.unk7, self.unk8))
		of.write(self.unk9)		
		for m in self.materials:
			of.write(struct.pack("<II", *m))
		of.write(self.strings)
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "materials ({})".format(len(self.materials)) # TODO: more like material maps paths? textures paths?

	def _get_string(self, start):
		i = start
		s = ""
		while i < len(self.strings):
			b = self.strings[i]
			if b == '\0':
				break
			s += b
			i += 1
		return s

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Materials    | {:6} values".format(self.TAG, len(self.materials))

		print self.data_size, self.unk1, self.unk2, self.unk3, self.unk4
		print self.materials_count, self.unk5, self.unk6, self.unk7, self.unk8
		print repr(self.unk9)

		
		print ""
		#######........ | 123
		print "           #    name"
		print "         -----------"
		for i in xrange(len(self.materials)):
			spos, shash = self.materials[i]

			s = self._get_string(spos)
			if s is None:
				s = "<str at {}>".format(spos)

			print "         - {:<3}  {:08X} {:08X}  {:<4}  {}".format(i, shash, crc32.hash(s, False), spos, s)
		print ""

#

class xD9B12454_Section(dat1lib.types.sections.Section):
	TAG = 0xD9B12454
	TYPE = 'Material'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 8 occurrences in 13178 files
		# size = 52
		#
		# examples: 891E22BD4A6EA203
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "D9B12454 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | D9B12454     | {:6} entries".format(self.TAG, len(self.entries))

#

class x3E45AA13_Section(dat1lib.types.sections.Section):
	TAG = 0x3E45AA13
	TYPE = 'Material'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3481 occurrences in 13178 files
		# size = 520
		#
		# examples: 8000E61F841EBC5F
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "3E45AA13 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 3E45AA13     | {:6} entries".format(self.TAG, len(self.entries))

#

class xE1275683_Section(dat1lib.types.sections.Section):
	TAG = 0xE1275683
	TYPE = 'Material'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 13178 occurrences in 13178 files (always present)
		# size = 40
		# always first
		#
		# examples: 8000B10F551366C6
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "E1275683 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | E1275683     | {:6} entries".format(self.TAG, len(self.entries))
