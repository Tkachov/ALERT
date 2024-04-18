# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

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

		ENTRY_SIZE = 48
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<4IQ6I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]
		# bones_count, unk1, unk2, unk3, modelname_hash, 0s

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<4IQ6I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "D614B18B ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | D614B18B     | {:6} entries".format(self.TAG, len(self.entries)))
		print()
		print("    #  model_name_hash   bones     #1    #2    #3    #4    #5    #6    #7    #8    #9")
		print(" -------------------------------------------------------------------------------------")
		for i, x in enumerate(self.entries):
			print("  - {}  {:016X}  {:5}  {:5} {:5} {:5} {:5} {:5} {:5} {:5} {:5} {:5}".format(i, x[4], x[0], x[1], x[2], x[3], x[5], x[6], x[7], x[8], x[9], x[10]))
		print()

#

class AnimDriverVarInfoSection(dat1lib.types.sections.Section):
	TAG = 0xDF74DA06 # Anim Driver Var Info
	TYPE = 'AnimSet_PerformanceSet'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 64 occurrences in 901 files
		# size = 12..3504 (avg = 255.1)
		#
		# examples: 10DD7F51 (min size), EA60260B (max size)

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
