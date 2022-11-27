import dat1lib.crc32 as crc32
import dat1lib.types.sections
import io
import json
import struct

class x81999057_Section(dat1lib.types.sections.SerializedSection):
	TAG = 0x81999057
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)

		# MSMR
		# 4959 occurrences in 12274 files
		# size = 32..600556 (avg = 7038.5)
		#
		# examples: 8015DB31E416FA83 (min size), AB72D30DF307A8DF (max size)

		# MM
		# 3802 occurrences in 10473 files
		# size = 16..2121056 (avg = 10334.6)
		#
		# examples: 9F4641AD3DDF206F (min size), 819B7068967A6DB9 (max size)

	def get_short_suffix(self):
		return "81999057"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 81999057     |".format(self.TAG))
		print(json.dumps(self.root, indent=4, sort_keys=True))
		if len(self.extras) > 0:
			print(" "*10, self.extras)

	def web_repr(self):
		return {"name": "81999057", "type": "json", "readonly": True, "content": self.root}

###

class x2300D240_Section(dat1lib.types.sections.SerializedSection):
	TAG = 0x2300D240
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)

		# MSMR
		# 2929 occurrences in 12274 files
		# size = 16..128176 (avg = 3318.0)
		#
		# examples: 92A2BFF3FD07FB68 (min size), 9D199DA44247F6C3 (max size)

		# MM
		# 1673 occurrences in 10473 files
		# size = 16..96168 (avg = 2614.8)
		#
		# examples: 87B81FEDAAFF3E8A (min size), BE5CA03295D3CE1E (max size)

	def get_short_suffix(self):
		return "2300D240"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 2300D240     |".format(self.TAG))
		print(json.dumps(self.root, indent=4, sort_keys=True))
		if len(self.extras) > 0:
			print(" "*10, self.extras)

	def web_repr(self):
		return {"name": "2300D240", "type": "json", "readonly": True, "content": self.root}
