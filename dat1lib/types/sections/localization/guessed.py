import dat1lib.types.sections
import io
import struct

class EntriesCountSection(dat1lib.types.sections.Section):
	TAG = 0xD540A903
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 4
		# always first
		#
		# examples: BE55D94F171BF8DE

		self.count = struct.unpack("<I", data)[0]

	def save(self):
		return struct.pack("<I", self.count)

	def get_short_suffix(self):
		return "entries count = {}".format(self.count)

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Entries Cnt  | = {}".format(self.TAG, self.count)

#

class KeyNamesSection(dat1lib.types.sections.StringsSection):
	TAG = 0x4D73CEBD
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.StringsSection.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 1348825
		#
		# examples: BE55D94F171BF8DE

	def get_short_suffix(self):
		return "key names ({})".format(len(self._strings))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Key Names    | {:6} strings".format(self.TAG, len(self._strings))
		if False:
			for s in self._strings:
				print " "*11 + "- '{}'".format(s)
			print ""

#

class ValuesSection(dat1lib.types.sections.StringsSection):
	TAG = 0x70A382B8
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.StringsSection.__init__(self, data, container)

		# 23 occurrences in 23 files (always present)
		# size = 3039405..4903208 (avg = 3404552.5)
		# always last
		#
		# examples: BE55D94F171BF8DE (min size), BE55D94F171BF8DE (max size)

	def get_short_suffix(self):
		return "values ({})".format(len(self._strings))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Values       | {:6} strings".format(self.TAG, len(self._strings))
		if False:
			for s in self._strings:
				print " "*11 + "- '{}'".format(s)
			print ""
