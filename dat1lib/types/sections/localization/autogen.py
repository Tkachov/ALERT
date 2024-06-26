# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

#

class x06A58050_Section(dat1lib.types.sections.Section):
	TAG = 0x06A58050
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 23 occurrences in 23 files (always present)
		# size = 229472
		#
		# examples: BE55D94F171BF8DE

		# MM
		# 32 occurrences in 32 files (always present)
		# size = 140480
		#
		# examples: BE55D94F171BF8DE

		# RCRA
		# 32 occurrences in 32 files (always present)
		# size = 98300
		#
		# examples: BE55D94F171BF8DE
		
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
		return "06A58050 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 06A58050     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x0CD2CFE9_Section(dat1lib.types.sections.Section):
	TAG = 0x0CD2CFE9 # Localization SortedIndexes Built
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 23 occurrences in 23 files (always present)
		# size = 114736
		#
		# examples: BE55D94F171BF8DE

		# MM
		# 32 occurrences in 32 files (always present)
		# size = 70240
		#
		# examples: BE55D94F171BF8DE

		# RCRA
		# 32 occurrences in 32 files (always present)
		# size = 49150
		#
		# examples: BE55D94F171BF8DE
		
		ENTRY_SIZE = 2
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<H", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<H", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "0CD2CFE9 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 0CD2CFE9     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xA4EA55B2_Section(dat1lib.types.sections.Section):
	TAG = 0xA4EA55B2 # Localization TagOffsets Built
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 23 occurrences in 23 files (always present)
		# size = 229472
		#
		# examples: BE55D94F171BF8DE

		# MM
		# 32 occurrences in 32 files (always present)
		# size = 140480
		#
		# examples: BE55D94F171BF8DE

		# RCRA
		# 32 occurrences in 32 files (always present)
		# size = 98300
		#
		# examples: BE55D94F171BF8DE
		
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
		return "A4EA55B2 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | A4EA55B2     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xB0653243_Section(dat1lib.types.sections.Section):
	TAG = 0xB0653243 # Localization Flags Built
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 23 occurrences in 23 files (always present)
		# size = 229472
		#
		# examples: BE55D94F171BF8DE

		# MM
		# 32 occurrences in 32 files (always present)
		# size = 140480
		#
		# examples: BE55D94F171BF8DE

		# RCRA
		# 32 occurrences in 32 files (always present)
		# size = 98300
		#
		# examples: BE55D94F171BF8DE
		
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
		return "B0653243 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | B0653243     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xC43731B5_Section(dat1lib.types.sections.Section):
	TAG = 0xC43731B5 # Localization SortedHashes Built
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 23 occurrences in 23 files (always present)
		# size = 229472
		#
		# examples: BE55D94F171BF8DE

		# MM
		# 32 occurrences in 32 files (always present)
		# size = 140480
		#
		# examples: BE55D94F171BF8DE

		# RCRA
		# 32 occurrences in 32 files (always present)
		# size = 98300
		#
		# examples: BE55D94F171BF8DE
		
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
		return "C43731B5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | C43731B5     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xF80DEEB4_Section(dat1lib.types.sections.Section):
	TAG = 0xF80DEEB4 # Localization TextOffsets Built
	TYPE = 'Localization'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 23 occurrences in 23 files (always present)
		# size = 229472
		#
		# examples: BE55D94F171BF8DE

		# MM
		# 32 occurrences in 32 files (always present)
		# size = 140480
		#
		# examples: BE55D94F171BF8DE

		# RCRA
		# 32 occurrences in 32 files (always present)
		# size = 98300
		#
		# examples: BE55D94F171BF8DE
		
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
		return "F80DEEB4 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | F80DEEB4     | {:6} entries".format(self.TAG, len(self.entries)))
