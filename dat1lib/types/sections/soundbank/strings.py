import dat1lib.crc32 as crc32
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class StringsSection(dat1lib.types.sections.Section):
	TAG = 0x3E8490A3 # Sound Bank Strings
	TYPE = 'soundbank'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# asset original filename, and all Wwise object names ordered by FNV hash value

		# SO
		# 1473 occurrences in 1473 files (always present)
		# size = 32..84851 (avg = 3031.1)
		#
		# examples: D39E6518 (min size), 91C12D8E (max size)

		# MSMR
		# 1345 occurrences in 1345 files (always present)
		# size = 36..188456 (avg = 1981.2)
		#
		# examples: 9D2635C59FA63EF4 (min size), 826509A0F509A671 (max size)

		# MM
		# 1239 occurrences in 1239 files (always present)
		# size = 26..167447 (avg = 1559.3)
		#
		# examples: 8FA8E5C5DDC315C1 (min size), AA47C17532AF52AC (max size)

		# RCRA
		# 1218 occurrences in 1218 files (always present)
		# size = 26..83460 (avg = 1096.5)
		#
		# examples: 9257F71232118757 (min size), 8E7F2FAFC675D9EF (max size)

		self._strings = []
		self._strings_map = {}

		offset = 0
		start = 0
		while offset < len(data):
			if data[offset] == 0 or offset == len(data)-1:
				end = offset-1
				if data[offset] == 0:
					end = offset

				s = data[start:end].decode("utf-8")
				self._strings += [s]
				self._strings_map[start] = s

				offset += 1
				r = offset % 4
				if r > 0:
					offset += 4-r

				start = offset
				continue

			offset += 1

	def get_string(self, offset):
		return self._strings_map.get(offset, None)

	def get_string_by_index(self, ndx):
		if ndx < 0 or ndx >= len(self._strings):
			return None

		return self._strings[ndx]

	#

	def get_short_suffix(self):
		return "strings ({})".format(len(self._strings))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Strings      | {:6} strings".format(self.TAG, len(self._strings)))
		for s in self._strings:
			print(" "*11 + "- '{}'".format(s))
		print("")

	def web_repr(self):
		content = f"{len(self._strings)} strings\n\n"
		for s in self._strings:
			content += f" - '{s}'\n"
		content += "\n"
		return {"name": "Strings", "type": "text", "readonly": True, "content": content}
