# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

#

class x09DC30AB_Section(dat1lib.types.sections.Section):
	TAG = 0x09DC30AB # Anim Clip Curves
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# size = 240
		#
		# examples: 846B8D250F1A33D2

		# MM: none

		# RCRA
		# size = 240
		#
		# examples: 846B8D250F1A33D2
		
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
		return "09DC30AB ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 09DC30AB     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x1722FAEF_Section(dat1lib.types.sections.Section):
	TAG = 0x1722FAEF # Anim Clip Geom Samples
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2 occurrences in 101563 files
		# size = 5712..7336 (avg = 6524.0)
		#
		# examples: 8478A801813D8B7F (min size), 9C473DAA0CFA8C46 (max size)

		# MM
		# 49 occurrences in 63110 files
		# size = 728..12936 (avg = 4690.2)
		#
		# examples: A2ED2F2FD3906DFB (min size), ADFE38EE70377E0D (max size)

		# RCRA
		# 7 occurrences in 37725 files
		# size = 1904..6720 (avg = 3568.0)
		#
		# examples: AEE3D0DF5CC8FED8 (min size), 9077925BD48F8496 (max size)
		
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
		return "1722FAEF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 1722FAEF     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x116EB684_Section(dat1lib.types.sections.Section):
	TAG = 0x116EB684 # Anim Clip Custom Track Data
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 19529 occurrences in 101563 files
		# size = 4..109604 (avg = 2610.5)
		#
		# examples: 800348B37A689421 (min size), 9CE2AD1BCB4DB00E (max size)

		# MM
		# 16187 occurrences in 63110 files
		# size = 4..117844 (avg = 2108.9)
		#
		# examples: 800E090BA1F2F337 (min size), 8B038DAAABCCA192 (max size)

		# RCRA
		# 2826 occurrences in 37725 files
		# size = 4..17664 (avg = 328.1)
		#
		# examples: 80072AF3C3605363 (min size), A72EC37700131823 (max size)
		
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
		return "116EB684 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 116EB684     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x2BB5BC8F_Section(dat1lib.types.sections.Section): # bone transforms (Qxyzw, xyz), same order as hashes in A3B26640?
	TAG = 0x2BB5BC8F # Anim Clip Base State
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 55174 occurrences in 101563 files
		# size = 4..50864 (avg = 1819.7)
		#
		# examples: 85488D6D1544D17F (min size), 9E3C7901446279A4 (max size)

		# MM
		# 37247 occurrences in 63110 files
		# size = 4..50128 (avg = 2329.9)
		#
		# examples: 80D58BB1AA4B6368 (min size), 8EE1B61ADADF360C (max size)

		# RCRA
		# 21377 occurrences in 37725 files
		# size = 16..7920 (avg = 2109.8)
		#
		# examples: 800CB253D80046C5 (min size), B816421C1D9E1D71 (max size)
		
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
		return "2BB5BC8F ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 2BB5BC8F     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x14014CB6_Section(dat1lib.types.sections.Section):
	TAG = 0x14014CB6 # Anim Clip Custom Tracks
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 19529 occurrences in 101563 files
		# size = 40..1560 (avg = 353.0)
		#
		# examples: 800348B37A689421 (min size), A06C251781E05522 (max size)

		# MM
		# 16187 occurrences in 63110 files
		# size = 40..1560 (avg = 240.0)
		#
		# examples: 800E090BA1F2F337 (min size), 815B25AB2285CEA5 (max size)

		# RCRA
		# 2826 occurrences in 37725 files
		# size = 40..640 (avg = 74.9)
		#
		# examples: 80072AF3C3605363 (min size), 86B7FF162ACB9CE1 (max size)
		
		ENTRY_SIZE = 40
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<10I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<10I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "14014CB6 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 14014CB6     | {:6} entries".format(self.TAG, len(self.entries)))

		print("")
		#######........ | 123  12345678  
		print("           #        hash  name")
		print("         -------------------------------------------------------------------------")
		for i, l in enumerate(self.entries):
			print("         - {:<3}  {:08X}  {}  {}".format(i, l[0], self._dat1._strings_map.get(l[1], None), l[2:]))
			# l[2], l[3] -- zeros
			# l[4] -- offset in 116EB684?
			# l[5] -- 257 (== count of bones?)
			# l[6], l[7] -- zeros
			# l[8] -- 1 or 69, affects offset in l[4] (1 is 16 bytes, 69 is 288 bytes)
			# l[9] -- zero

		print("")

#

class x1D4BD9FA_Section(dat1lib.types.sections.Section):
	TAG = 0x1D4BD9FA # Anim Clip Pose Phoneme Visems Map
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 21 occurrences in 101563 files
		# size = 80
		#
		# examples: 822F805090E0E20C

		# MM
		# 14 occurrences in 63110 files
		# size = 80
		#
		# examples: 822F805090E0E20C

		# RCRA
		# 22 occurrences in 37725 files
		# size = 80
		#
		# examples: 802E2F66998AF7A7
		
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
		return "1D4BD9FA ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 1D4BD9FA     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x3A7B4855_Section(dat1lib.types.sections.Section):
	TAG = 0x3A7B4855 # Anim Clip Sample Data
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 63769 occurrences in 101563 files
		# size = 8..16548472 (avg = 11694.2)
		#
		# examples: 86A064510C89C158 (min size), 975FE295868E3A97 (max size)

		# MM
		# 44675 occurrences in 63110 files
		# size = 8..5656800 (avg = 15564.9)
		#
		# examples: 86A064510C89C158 (min size), 8EE1B61ADADF360C (max size)

		# RCRA
		# 27189 occurrences in 37725 files
		# size = 8..964200 (avg = 10988.4)
		#
		# examples: 91A3191CF63F6E80 (min size), 95FFCDC9FC52BAEE (max size)
		
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
		return "3A7B4855 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 3A7B4855     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x3976E44C_Section(dat1lib.types.sections.Section):
	TAG = 0x3976E44C # Anim Clip Path
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 59909 occurrences in 101563 files
		# size = 128
		#
		# examples: 80006FCEB83F81B3

		# MM
		# 40325 occurrences in 63110 files
		# size = 128
		#
		# examples: 80006FCEB83F81B3

		# RCRA
		# 23295 occurrences in 37725 files
		# size = 128
		#
		# examples: 80000DCC5F02623C

		# two matrixes 4x4 (like I + translation vector)
		
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
		return "3976E44C ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 3976E44C     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x277563F5_Section(dat1lib.types.sections.Section):
	TAG = 0x277563F5 # Anim Clip Morph Info
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 10031 occurrences in 101563 files
		# size = 28..7880 (avg = 544.8)
		#
		# examples: 818633D976D7F2F7 (min size), 9CE2AD1BCB4DB00E (max size)

		# MM
		# 9698 occurrences in 63110 files
		# size = 28..9896 (avg = 384.7)
		#
		# examples: 84AF739FC0612DEE (min size), 8F179913F5F49D19 (max size)

		# RCRA
		# 2821 occurrences in 37725 files
		# size = 28..3488 (avg = 610.1)
		#
		# examples: 9235F21D749D5544 (min size), A1B51C94AE45572C (max size)
		
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
		return "277563F5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 277563F5     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x4FC98D7E_Section(dat1lib.types.sections.Section):
	TAG = 0x4FC98D7E # Anim Clip Curves Data
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# size = 93604
		#
		# examples: 846B8D250F1A33D2

		# MM: none

		# RCRA
		# size = 93604
		#
		# examples: 846B8D250F1A33D2
		
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
		return "4FC98D7E ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 4FC98D7E     | {:6} entries".format(self.TAG, len(self.entries)))

#

class AnimClipBuiltSection(dat1lib.types.sections.Section):
	TAG = 0x9DF23F77 # Anim Clip Built
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 101557 occurrences in 101563 files
		# size = 96
		#
		# examples: 80006FCEB83F81B3

		# MM
		# 62720 occurrences in 63110 files
		# size = 96
		#
		# examples: 800032F7B1757E90

		# RCRA
		# 37697 occurrences in 37725 files
		# size = 96
		#
		# examples: 80000DCC5F02623C
		
		"""
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]
		"""
		self.entries = struct.unpack("<I46H", data)

	"""
	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()
	"""

	def get_short_suffix(self):
		return "Anim Clip Built ({})".format(len(self.entries))

	def print_verbose(self, config):		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Clip Built   |".format(self.TAG))

		print(" "*10, self._dat1._strings_map.get(self.entries[0], None)) #  self._dat1.get_string(self.entries[0]))

		prefixes = {
			9: "bones count (A3B26640)",
			15: "bones count (A3B26640)",
			17: "? count (D070D358)",
			28: "anims count (14014CB6)" # "custom tracks"
		}

		for i in range(1, 46):
			pref = ""
			if i in prefixes:
				pref = " -- " + prefixes[i]
			print(" "*10, "{0:5} {0:04X}{1}".format(self.entries[i], pref))

#

class x411852D5_Section(dat1lib.types.sections.Section):
	TAG = 0x411852D5 # Anim Clip Geom Sample Data
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2 occurrences in 101563 files
		# size = 83090..9912360 (avg = 4997725.0)
		#
		# examples: 9C473DAA0CFA8C46 (min size), 8478A801813D8B7F (max size)

		# MM
		# 49 occurrences in 63110 files
		# size = 18179..11296493 (avg = 887222.6)
		#
		# examples: 9CDE17E2684A7AFE (min size), 9F2D52FB01A4D401 (max size)

		# RCRA
		# 7 occurrences in 37725 files
		# size = 812312..11588125 (avg = 4461274.7)
		#
		# examples: 9077925BD48F8496 (min size), B582E825EF5E4B7C (max size)
		pass

	def get_short_suffix(self):
		return "411852D5 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 411852D5     | {:6} bytes".format(self.TAG, len(self._raw)))

#

class xA3B26640_Section(dat1lib.types.sections.Section): # bone hashes
	TAG = 0xA3B26640 # Anim Clip Joint Hashes
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 55174 occurrences in 101563 files
		# size = 8..12712 (avg = 442.1)
		#
		# examples: 8004B281B238C4AB (min size), 9E3C7901446279A4 (max size)

		# MM
		# 37247 occurrences in 63110 files
		# size = 8..12536 (avg = 577.4)
		#
		# examples: 80008A8237FD3B4C (min size), 8EE1B61ADADF360C (max size)

		# RCRA
		# 21377 occurrences in 37725 files
		# size = 8..1824 (avg = 510.9)
		#
		# examples: 800CB253D80046C5 (min size), 801F365EC4F8F471 (max size)

		# always goes with 2BB5BC8F
		
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
		return "A3B26640 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | A3B26640     | {:6} entries".format(self.TAG, len(self.entries)))

		print("")
		#######........ | 123  12345678
		print("           #    bonehash")
		print("         ----------------")
		for i, e in enumerate(self.entries):
			print("         - {:<3}  {:08X}".format(i, e))

		print("")


#

class AnimClipTriggerDataSection(dat1lib.types.sections.Section):
	TAG = 0x6962F7DE # Anim Clip Trigger Data
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.extra = struct.unpack("<4I", data[:16])
		self.jsons = None
		try:
			self.jsons = dat1lib.types.sections.SerializedSection(data[16:], self._dat1)
		except:
			pass

		# MSMR
		# 9621 occurrences in 101563 files
		# size = 32..36352 (avg = 809.9)
		#
		# examples: 8016138A3C568830 (min size), 85AA1DDD57D6B350 (max size)

		# MM
		# 12792 occurrences in 63110 files
		# size = 32..34224 (avg = 1060.4)
		#
		# examples: 8016138A3C568830 (min size), 85AA1DDD57D6B350 (max size)

		# RCRA
		# 4674 occurrences in 37725 files
		# size = 32..9976 (avg = 630.8)
		#
		# examples: 800CF2F9CDB8A233 (min size), BA15E7BF3250F92A (max size)

	def get_short_suffix(self):
		return "Anim Clip Trigger Data"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Trigger Data |".format(self.TAG))
		print(" "*10, self.extra)
		try:
			print(" "*10, self.jsons.root)
			if len(self.jsons.extras) > 0:
				print(" "*10, self.jsons.extras)
		except:
			pass

#

class x495BA079_Section(dat1lib.types.sections.Section):
	TAG = 0x495BA079 # Anim Clip Pose Expression Id Map
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 21 occurrences in 101563 files
		# size = 104..272 (avg = 216.3)
		#
		# examples: 8B02253D6E768605 (min size), 822F805090E0E20C (max size)

		# MM
		# 14 occurrences in 63110 files
		# size = 128..272 (avg = 240.0)
		#
		# examples: 9AF5A87238CA90E7 (min size), 8252C34748BB26FD (max size)

		# RCRA
		# 22 occurrences in 37725 files
		# size = 104..192 (avg = 111.6)
		#
		# examples: 8282B743F97BAAB1 (min size), B5974BED8417ABEB (max size)
		
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
		return "495BA079 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 495BA079     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xE08AA35F_Section(dat1lib.types.sections.Section):
	TAG = 0xE08AA35F # Anim Clip Motion Data
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 59930 occurrences in 101563 files
		# size = 128..51680 (avg = 892.0)
		#
		# examples: 8000839F16C48791 (min size), 9A967494A921B89B (max size)

		# MM
		# 40339 occurrences in 63110 files
		# size = 128..49888 (avg = 1103.6)
		#
		# examples: 80008A737EDB7027 (min size), 8BC7BE16E30D9D0E (max size)

		# RCRA
		# 23317 occurrences in 37725 files
		# size = 128..43232 (avg = 1136.7)
		#
		# examples: 80000DCC5F02623C (min size), A9B916311A794FB0 (max size)
		
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
		return "E08AA35F ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | E08AA35F     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x69F64588_Section(dat1lib.types.sections.Section):
	TAG = 0x69F64588 # Anim Clip Morph Frame Data
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 10031 occurrences in 101563 files
		# size = 4..335984 (avg = 3692.1)
		#
		# examples: 841D3C3D13D24ED2 (min size), 835C8B5CA6E9FCD2 (max size)

		# MM
		# 9698 occurrences in 63110 files
		# size = 8..393112 (avg = 2857.3)
		#
		# examples: 8342F7F41131BB7F (min size), 8B038DAAABCCA192 (max size)

		# RCRA
		# 2821 occurrences in 37725 files
		# size = 4..123876 (avg = 5690.2)
		#
		# examples: B16E73902A8C1B94 (min size), A1B51C94AE45572C (max size)
		
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
		return "69F64588 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 69F64588     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x74FC0175_Section(dat1lib.types.sections.Section):
	TAG = 0x74FC0175 # Anim Clip Trigger Joint Names
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 3450 occurrences in 101563 files
		# size = 4..16 (avg = 4.0)
		#
		# examples: 80006FCEB83F81B3 (min size), A7E18BFCA6DA9B17 (max size)

		# MM
		# 2441 occurrences in 63110 files
		# size = 4..16 (avg = 4.4)
		#
		# examples: 80114FA50C1ED5A7 (min size), 801292E8481D4ADD (max size)

		# RCRA
		# 76 occurrences in 37725 files
		# size = 4..8 (avg = 7.2)
		#
		# examples: 89816BEB1EB099C3 (min size), 8051793D7FCAD3CA (max size)
		
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
		return "74FC0175 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 74FC0175     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xD070D358_Section(dat1lib.types.sections.Section):
	TAG = 0xD070D358 # Anim Clip Sample Elem
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 22140 occurrences in 101563 files
		# size = 8..87748 (avg = 2005.7)
		#
		# examples: 802DBD52E23D275C (min size), 975FE295868E3A97 (max size)

		# MM
		# 22257 occurrences in 63110 files
		# size = 8..76736 (avg = 1634.5)
		#
		# examples: 800E6D4C6EE30DC5 (min size), 8EE1B61ADADF360C (max size)

		# RCRA
		# 12809 occurrences in 37725 files
		# size = 8..7292 (avg = 1245.8)
		#
		# examples: 80222B516C5D83E8 (min size), B816421C1D9E1D71 (max size)
		
		ENTRY_SIZE = 5
		count = len(data)//ENTRY_SIZE

		ENTRY_SIZE = 4
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

		offset = ENTRY_SIZE * count
		ENTRY_SIZE = 1
		self.entries2 = [struct.unpack("<B", data[offset+i*ENTRY_SIZE:offset+(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	"""
	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		for e in self.entries2:
			of.write(struct.pack("<B", e))
		for i in range((4 - (len(self.entries)%4))%4):
			of.write(b'\x00')
		of.seek(0)
		return of.read()
	"""

	def get_short_suffix(self):
		return "D070D358 ({})".format(len(self.entries))

	def print_verbose(self, config):		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | D070D358     | {:6} entries".format(self.TAG, len(self.entries)))

		print("")
		#######........ | 123  12345678  123
		print("           #        hash  ndx")
		print("         ---------------------")
		for i, l in enumerate(self.entries):
			print("         - {:<3}  {:08X}  {}".format(i, l, self.entries2[i]))
		print("")
