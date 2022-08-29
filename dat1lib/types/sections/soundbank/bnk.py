import dat1lib.types.sections
import io
import struct

class BinkSection(dat1lib.types.sections.Section):
	TAG = 0x53F25238
	TYPE = 'soundbank'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

	def replace_data(self, data):
		self._raw = data

	def get_short_suffix(self):
		return ".bnk"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Bink Data    |".format(self.TAG)
