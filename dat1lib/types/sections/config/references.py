import dat1lib.crc64 as crc64
import dat1lib.types.sections
import io
import struct

class ReferencesSection(dat1lib.types.sections.ReferencesSection):
	TAG = 0x58B8558A # Config Asset Refs
	TYPE = 'config'

	def __init__(self, data, container):
		dat1lib.types.sections.ReferencesSection.__init__(self, data, container)

		# MSMR
		# 1276 occurrences in 2521 files
		# size = 16..6336 (avg = 100.3)
		#
		# examples: 8008619CBD504B56 (min size), A2E15A1561AF23C6 (max size)

		# MM
		# 1006 occurrences in 2026 files
		# size = 16..6464 (avg = 117.8)
		#
		# examples: 804666DEE5E1774A (min size), AED6101948AAFA54 (max size)

		# RCRA
		# 717 occurrences in 1847 files
		# size = 16..7184 (avg = 101.4)
		#
		# examples: 8027BEC8CB618B30 (min size), AED6101948AAFA54 (max size)

	def get_short_suffix(self):
		return "Config Asset Refs ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | References   | {:6} entries".format(self.TAG, len(self.entries)))
		dat1lib.types.sections.ReferencesSection.print_verbose(self, config)
