import dat1lib.crc64 as crc64
import dat1lib.types.sections
import io
import struct

class x364A6C7C_Section(dat1lib.types.sections.Section):
	TAG = 0x364A6C7C
	TYPE = 'Actor'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 2568 occurrences in 2568 files (always present)
		# size = 112..184 (avg = 168.2)
		#
		# examples: 01668585 (min size), 18D35F13 (max size)

		# MSMR
		# 5167 occurrences in 5167 files (always present)
		# size = 176..320 (avg = 301.3)
		#
		# examples: 802A792FD6F72CE3 (min size), 80029DC4DB44B189 (max size)

		# MM
		# 3793 occurrences in 3793 files (always present)
		# size = 176..320 (avg = 302.6)
		#
		# examples: 8090DFC5CFCD7795 (min size), 80027411351D35BA (max size)

		# RCRA
		# 2696 occurrences in 2696 files (always present)
		# size = 176..320 (avg = 294.3)
		#
		# examples: 8019B5E20240AA66 (min size), 80081F701B415E30 (max size)

		# floats; starts with 4x4 matrix (identity in actors_3d_poi_distant_fx_marker_quest_vertical_camfacer.actor)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "364A6C7C ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return

		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 364A6C7C     | {:6} entries".format(self.TAG, len(self.entries)))
		for i, x in enumerate(self.entries):
			print("  - {:<3}  {:08X} {}".format(i, x, x))
		print("")
