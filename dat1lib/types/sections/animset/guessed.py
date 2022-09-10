import dat1lib.crc32 as crc32
import dat1lib.types.sections
import io
import struct

class SomeBonesInfoSection(dat1lib.types.sections.Section):
	TAG = 0x42F16D0C
	TYPE = 'AnimSet_PerformanceSet'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 499 occurrences in 1683 files
		# size = 96..107040 (avg = 7291.3)
		#
		# examples: 96AD98C8AC61B09A (min size), A8052A228EF425FE (max size)
		
		ENTRY_SIZE = 12
		self.entries = []
		i = 0
		while True:
			a, b, c, d = struct.unpack("<IIhh", data[i:i+ENTRY_SIZE])
			i += ENTRY_SIZE
			if a == 0xFFFFFFFF and b == 0xFFFFFFFF and c == -1 and d == 0:
				break
			self.entries += [(a, b, c, d)]

		self.values = []
		while True:
			a, b, c = struct.unpack("<III", data[i:i+ENTRY_SIZE])
			i += ENTRY_SIZE
			if len(self.values) > 0 and a == 0 and b == 0 and c == 0:
				break
			self.values += [(a, b, c)]

		ENTRY_SIZE = 8
		self.values2 = []
		for j in xrange(len(self.values)):
			a, b = struct.unpack("<II", data[i:i+ENTRY_SIZE])
			i += ENTRY_SIZE
			self.values2 += [(a, b)]

		self.rest_offset = i
		self.rest = data[self.rest_offset:]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def _get_string(self, start):
		i = start - self.rest_offset
		s = ""
		while i < len(self.rest):
			b = self.rest[i]
			if b == '\0':
				break
			s += b
			i += 1
		return s

	def get_short_suffix(self):
		return "some bones info ({}, {})".format(len(self.entries), len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Bones Info   | {:6} bones, {:6} entries".format(self.TAG, len(self.entries), len(self.values))
		for i, x in enumerate(self.entries):
			s = self._get_string(x[1])
			# print "  - {:<3}  {:3}  {}".format(i, x[2], s)
			print "  - {:<3}  {:3}  {:08X} {}".format(i, x[2], x[0], s)

			if config.get("section_warnings", True):
				if s is not None:
					real_hash = crc32.hash(s, False)
					if real_hash != x[0]:
						print "        [!] filename real hash {:08X} is not equal to one written in the struct {:08X}".format(real_hash, x[0])
		print ""
		for i, ((a,b,c), (d,e)) in enumerate(zip(self.values, self.values2)):
			print "  - {:<3}  {:08X}  {:08X}  {:08X}  |  {:08X}  {:08X}".format(i, a,b,c,d,e)
		# print self.rest_offset, repr(self.rest)
		print ""
