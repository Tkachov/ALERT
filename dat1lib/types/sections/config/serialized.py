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

	def get_short_suffix(self):
		return "content"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Content      |".format(self.TAG)
		print json.dumps(self.root, indent=4, sort_keys=True)
		if len(self.extras) > 0:
			print " "*10, self.extras
