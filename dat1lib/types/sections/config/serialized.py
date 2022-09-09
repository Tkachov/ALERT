import dat1lib.crc32 as crc32
import dat1lib.types.sections
import io
import json
import struct

class ConfigTypeSection(dat1lib.types.sections.SerializedSection):
	TAG = 0x4A128222
	TYPE = 'config'

	def __init__(self, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)

		# 2521 occurrences in 2521 files (always present)
		# size = 56..84 (avg = 65.1)
		# always first
		#
		# examples: 80880A03CBA9B6B0 (min size), 852FD4D4179A4F46 (max size)

	def get_short_suffix(self):
		return "type"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Config Type  | {}".format(self.TAG, self.root)
		if len(self.extras) > 0:
			print " "*10, self.extras

###

class ConfigContentSection(dat1lib.types.sections.SerializedSection):
	TAG = 0xE501186F
	TYPE = 'config'

	def __init__(self, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)

		# 2521 occurrences in 2521 files (always present)
		# size = 16..975836 (avg = 3205.9)
		#
		# examples: 813381135A2CC078 (min size), A5C3BBB75C76D0FA (max size)

	def get_short_suffix(self):
		return "content"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Content      |".format(self.TAG)
		print json.dumps(self.root, indent=4, sort_keys=True)
		if len(self.extras) > 0:
			print " "*10, self.extras
