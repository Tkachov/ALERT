import dat1lib.types.sections
import io
import struct

class WwiseBankSection(dat1lib.types.sections.Section):
	TAG = 0x53F25238
	TYPE = 'soundbank'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1345 occurrences in 1345 files (always present)
		# size = 32..29272753 (avg = 769806.9)
		# always last
		#
		# examples: 8C129CA7DA42BEAE (min size), 9B3473B5F2EF53D3 (max size)

	def replace_data(self, data):
		self._raw = data

	def get_short_suffix(self):
		return ".bnk"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Wwise Bank   |".format(self.TAG))
