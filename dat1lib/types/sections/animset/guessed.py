import dat1lib.crc32 as crc32
import dat1lib.types.sections
import io
import struct

class SomeBonesInfoSection(dat1lib.types.sections.Section):
	TAG = 0x42F16D0C
	TYPE = 'AnimSet_PerformanceSet'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 499 occurrences in 1683 files
		# size = 96..107040 (avg = 7291.3)
		#
		# examples: 96AD98C8AC61B09A (min size), A8052A228EF425FE (max size)

		# MM
		# 408 occurrences in 953 files
		# size = 96..106064 (avg = 6200.8)
		#
		# examples: 96AD98C8AC61B09A (min size), AC4A301352BCC79B (max size)

		# RCRA
		# 380 occurrences in 787 files
		# size = 96..14592 (avg = 4217.6)
		#
		# examples: 8A7DB48B384467EF (min size), 802FF1404940D6AA (max size)

		# s = container.get_section(0xD614B18B)
		
		ENTRY_SIZE = 12
		self.entries = []
		i = 0
		while True:
			a, b, c, d = struct.unpack("<IIhh", data[i:i+ENTRY_SIZE])
			i += ENTRY_SIZE
			# print(a, b, c, d)
			if a == 0xFFFFFFFF and b == 0xFFFFFFFF and c == -1 and d == 0:
				break
			self.entries += [(a, b, c, d)]

		"""
		self.values = []
		while i < s.unk2:
			a, b, c = struct.unpack("<III", data[i:i+ENTRY_SIZE])
			print(a, b, c)
			i += ENTRY_SIZE
			if len(self.values) > 0 and a == 0 and b == 0 and c == 0:
				break
			self.values += [(a, b, c)]

		ENTRY_SIZE = 8
		self.values2 = []
		for j in range(len(self.values)):
			a, b = struct.unpack("<II", data[i:i+ENTRY_SIZE])
			print(a, b)
			i += ENTRY_SIZE
			self.values2 += [(a, b)]
		"""

		self.rest_offset = i
		self.rest = data[self.rest_offset:]

	def _get_string(self, start):
		i = start - self.rest_offset
		s = bytearray()
		while i < len(self.rest):
			b = self.rest[i]
			if b == 0:
				break
			s.append(b)
			i += 1
		return s.decode('ascii')

	def get_short_suffix(self):
		# return "some bones info ({}, {})".format(len(self.entries), len(self.values))
		return "some bones info ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		# print("{:08X} | Bones Info   | {:6} bones, {:6} entries".format(self.TAG, len(self.entries), len(self.values)))
		print("{:08X} | Bones Info   | {:6} bones".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			s = self._get_string(x[1])
			# print("  - {:<3}  {:3}  {}".format(i, x[2], s))
			print("  - {:<3}  {:3}  {:08X} {}".format(i, x[2], x[0], s))

			if config.get("section_warnings", True):
				if s is not None:
					real_hash = crc32.hash(s, False)
					if real_hash != x[0]:
						print("        [!] filename real hash {:08X} is not equal to one written in the struct {:08X}".format(real_hash, x[0]))
		"""
		print("")
		for i, ((a,b,c), (d,e)) in enumerate(zip(self.values, self.values2)):
			print("  - {:<3}  {:08X}  {:08X}  {:08X}  |  {:08X}  {:08X}".format(i, a,b,c,d,e))
		"""
		# print(self.rest_offset, repr(self.rest))
		print("")
