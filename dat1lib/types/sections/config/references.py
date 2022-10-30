import dat1lib.crc64 as crc64
import dat1lib.types.sections
import io
import struct

class ReferencesSection(dat1lib.types.sections.Section):
	TAG = 0x58B8558A
	TYPE = 'config'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1276 occurrences in 2521 files
		# size = 16..6336 (avg = 100.3)
		#
		# examples: 8008619CBD504B56 (min size), A2E15A1561AF23C6 (max size)
		
		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<QII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<QII", *e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "references ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | References   | {:6} entries".format(self.TAG, len(self.entries)))

		EXTENSIONS_HASHES = {
			0xB5AAFACC: "Material", # crc32 of ".material"
			0xA9F149C4: "Config", # crc32 of ".config"
			0x37E72F50: "Actor"
		}

		for i, x in enumerate(self.entries):
			s = self._dat1.get_string(x[1])
			print("  - {:<2}  {:016X} {} {}".format(i, x[0], EXTENSIONS_HASHES.get(x[2], "{:08X}".format(x[2])), s))
			if config.get("section_warnings", True):
				if s is not None:
					real_hash = crc64.hash(s)
					if real_hash != x[0]:
						print("        [!] filename real hash {:016X} is not equal to one written in the struct {:016X}".format(real_hash, x[0]))
		print("")
