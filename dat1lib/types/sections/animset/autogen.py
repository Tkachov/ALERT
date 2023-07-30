import dat1lib.crc32 as crc32
import dat1lib.types.sections
import io
import struct

class xD614B18B_Section(dat1lib.types.sections.Section):
	TAG = 0xD614B18B
	TYPE = 'AnimSet_PerformanceSet'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 499 occurrences in 1683 files
		# size = 48..96 (avg = 52.8)
		#
		# examples: 80176C7A46F8A544 (min size), 817AFFAD64BE2622 (max size)

		# MM
		# 408 occurrences in 953 files
		# size = 48..96 (avg = 48.5)
		#
		# examples: 8019E233758A1721 (min size), 8066767AB8665577 (max size)

		# RCRA
		# 380 occurrences in 787 files
		# size = 48
		#
		# examples: 802FF1404940D6AA

		self.bones_count, self.unk1, self.unk2, self.unk3, self.modelname_hash = struct.unpack("<IIIIQ", data[:24])

		rest = data[24:]
		ENTRY_SIZE = 4
		count = len(rest)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", rest[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "D614B18B ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | D614B18B     | {:6} entries".format(self.TAG, len(self.entries)))
		print("bones={}, modelname_hash={:016X}, 0={}, ?={}, ?={}".format(self.bones_count, self.modelname_hash, self.unk1, self.unk2, self.unk3))
		for i, x in enumerate(self.entries):
			print("  - {:<3}  {:08X} {:10} {}".format(i, x, x, self._dat1.get_string(x)))
		print("")

#

class AnimDriverVarInfoSection(dat1lib.types.sections.Section):
	TAG = 0xDF74DA06 # Anim Driver Var Info
	TYPE = 'AnimSet_PerformanceSet'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 134 occurrences in 1683 files
		# size = 12..4992 (avg = 189.0)
		#
		# examples: 80B6332B78CB1955 (min size), 888DBF4798E4E906 (max size)

		# MM
		# 152 occurrences in 953 files
		# size = 12..9576 (avg = 306.4)
		#
		# examples: 83C59A32997D7F02 (min size), 829740303741E942 (max size)

		# RCRA
		# 84 occurrences in 787 files
		# size = 12..2160 (avg = 236.2)
		#
		# examples: 8B39F6A9A4A8C23A (min size), 8867CE5CFD9543DE (max size)
		
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
		return "Anim Driver Var Info ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Drvr VarInfo | {:6} entries".format(self.TAG, len(self.entries)))
