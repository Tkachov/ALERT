# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

"""
-------------------------------------------
  #  `tag`       offset      size   ends at
-------------------------------------------
- 0  7A0266BC  46461056    415097  46876152
- 1  933C0D32  41479872   3320776  44800647
- 2  BC91D1CC  48536560   5274820  53811379
- 3  BFEC699F  53811392     27580  53838971
- 4  D101A6CC  44800656   1660388  46461043
- 5  F958372E  46876160   1660388  48536547
"""

DEBUG_RANGE = range(10, 20)
DEBUG_RANGE = None

class AssetTypeSection(dat1lib.types.sections.Section):
	TAG = 0x7A0266BC # Asset Types
	TYPE = 'dag'

	KNOWN_TYPES = {
		0: "level", 1: "zone", 2: "actor", 3: "conduit", 4: "config",
		5: "cinematic2", 6: "model", 7: "animclip", 8: "animset", 9: "material",
		10: "materialgraph", 11: "texture", 12: "atmosphere", 13: "visualeffect", 14: "soundbank",
		15: "localization", 18: "zonelightbin", 19: "levellight", 20: "nodegraph",
		22: "wwiselookup"
	}

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.entries = data

	def get_short_suffix(self):
		return "types ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Types        | {:6} bytes".format(self.TAG, len(self.entries)))

		if DEBUG_RANGE is not None:
			print("")
			#######........ | 123  123
			print("           #      v  type")
			print("         ----------------")
			for i in DEBUG_RANGE:
				l = self.entries[i]
				print("         - {:<3}  {:3}  {}".format(i, l, self.KNOWN_TYPES.get(l, '?')))
			print("")

#

class x933C0D32_Section(dat1lib.types.sections.Section): # 8 bytes per entry
	TAG = 0x933C0D32 # Asset Ids
	TYPE = 'dag'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 8
		count = len(data) // ENTRY_SIZE
		self.entries = [struct.unpack("<II", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def get_short_suffix(self):
		return "? ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | pairs?       | {:6} pairs".format(self.TAG, len(self.entries)))

		if DEBUG_RANGE is not None:
			print("")
			#######........ | 123  12345678  12345678
			print("           #           a         b")
			print("         -------------------------")
			for i in DEBUG_RANGE:
				l = self.entries[i]
				print("         - {:<3}  {:08X}  {:08X}".format(i, l[0], l[1]))
			print("")

#

class AssetNamesSection(dat1lib.types.sections.Section): # TODO: dat1lib.types.sections.StringsReferencingSection
	TAG = 0xD101A6CC # Asset Names
	TYPE = 'dag'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 4
		count = len(data) // ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def get_short_suffix(self):
		return "Asset Names ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Asset Names  | {:6} values".format(self.TAG, len(self.entries)))

		if DEBUG_RANGE is not None:
			print("")
			#######........ | 123
			print("           #    name")
			print("         -----------")
			for i in DEBUG_RANGE:
				l = self.entries[i]

				s = self._dat1.get_string(l)
				if s is None:
					s = "<str at {}>".format(l)

				# print("         - {:<3}  {:08X}".format(i, l))
				if False:
					print("         - {:<3}  {:016X} {:08X}  {}".format(i, crc64.hash(s), crc32.hash(s), s))
				else:
					print("         - {:<3}  {}".format(i, s))
			print("")

#

class DependenciesSection(dat1lib.types.sections.Section): # 4 bytes index to what this asset is dependent to
	TAG = 0xF958372E # Dependency Links Heads
	TYPE = 'dag'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 4
		count = len(data) // ENTRY_SIZE
		self.entries = [struct.unpack("<i", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def get_short_suffix(self):
		return "parents ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Dependencies | {:6} values".format(self.TAG, len(self.entries)))

		if DEBUG_RANGE is not None:
			print("")
			#######........ | 123  12345678
			print("           #           v")
			print("         ---------------")
			for i in DEBUG_RANGE:
				l = self.entries[i]
				print("         - {:<3}  {:8}".format(i, l))
			print("")
#

class xBC91D1CC_Section(dat1lib.types.sections.Section): # longest section, looks like string offsets
	TAG = 0xBC91D1CC # Dependency Links
	TYPE = 'dag'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 8
		count = len(data) // ENTRY_SIZE
		self.entries = [struct.unpack("<ii", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def get_short_suffix(self):
		return "? ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | ?            | {:6} values".format(self.TAG, len(self.entries)))

		"""
		COLS_PER_ROW = 4
		for rows in range(4):
			print(" ".join(["{:8} {:8}".format(*self.entries[rows*COLS_PER_ROW + cols]) for cols in range(COLS_PER_ROW)]))
		"""
		def get_s(l):
			s = self._dat1.get_string(l)
			if s is None:
				s = "<str at {}>".format(l)
			return s

		for i in range(7):
			a, b = self.entries[i]
			sa, sb = get_s(a), get_s(b)
			print("  {:<3}  {:6} {}".format(i, a, sa))
			print("       {:6} {}".format(b, sb))
		print("")

		mna, mxa = -1, -1
		mnb, mxb = -1, -1
		for i in range(len(self.entries)):
			a, b = self.entries[i]
			if a != -1:
				if mna == -1 or self.entries[mna][0] > a:
					mna = i
				if mxa == -1 or self.entries[mxa][0] < a:
					mxa = i
			if b != -1:
				if mnb == -1 or self.entries[mnb][0] > b:
					mnb = i
				if mxb == -1 or self.entries[mxb][0] < b:
					mxb = i

		print("min at #{} = {}".format(mna, self.entries[mna]))
		print("max at #{} = {}".format(mxa, self.entries[mxa]))
		print("min at #{} = {}".format(mnb, self.entries[mnb]))
		print("max at #{} = {}".format(mxb, self.entries[mxb]))

#

class xBFEC699F_Section(dat1lib.types.sections.Section): # shortest section, some indexes
	TAG = 0xBFEC699F # LC Link Heads
	TYPE = 'dag'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 4
		count = len(data) // ENTRY_SIZE
		self.entries = [struct.unpack("<i", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def get_short_suffix(self):
		return "? ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | ?            | {:6} values".format(self.TAG, len(self.entries)))

		if False:
			COLS_PER_ROW = 1
			for i in range(2, 10):
				if len(self.entries) % i == 0:
					COLS_PER_ROW = i
			print("")
			for rows in range(len(self.entries) // COLS_PER_ROW):
				print(" ".join(["{:7}".format(self.entries[rows*COLS_PER_ROW + cols]) for cols in range(COLS_PER_ROW)]))
			print("")

		mn, mx = -1, -1
		prev = None
		only_asc = True
		for i in range(len(self.entries)):
			if self.entries[i] == -1:
				continue
			if mn == -1 or self.entries[mn] > self.entries[i]:
				mn = i
			if mx == -1 or self.entries[mx] < self.entries[i]:
				mx = i				
			if only_asc:
				if prev is not None:
					if prev > self.entries[i]:
						only_asc = False
				prev = self.entries[i]

		print("min at #{} = {}".format(mn, self.entries[mn]))
		print("max at #{} = {}".format(mx, self.entries[mx]))
		print("values always ascend = {} (ignoring -1s)".format(only_asc))
