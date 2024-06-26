# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

#

class x52B343E8_Section(dat1lib.types.sections.Section):
	TAG = 0x52B343E8
	TYPE = 'WwiseLookup'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# size = 15828
		# always first
		#
		# examples: A81AB0A616889CC2

		# MM
		# size = 13020
		# always first
		#
		# examples: A81AB0A616889CC2

		# RCRA
		# size = 12552
		# always first
		#
		# examples: A81AB0A616889CC2
		
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
		return "52B343E8 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 52B343E8     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x739B21E0_Section(dat1lib.types.sections.Section):
	TAG = 0x739B21E0
	TYPE = 'WwiseLookup'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# size = 1767744
		# always last
		#
		# examples: A81AB0A616889CC2

		# MM
		# size = 1155648
		# always last
		#
		# examples: A81AB0A616889CC2

		# RCRA
		# size = 775872
		# always last
		#
		# examples: A81AB0A616889CC2
		
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
		return "739B21E0 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 739B21E0     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x7F9A96AA_Section(dat1lib.types.sections.Section):
	TAG = 0x7F9A96AA
	TYPE = 'WwiseLookup'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# size = 220968
		#
		# examples: A81AB0A616889CC2

		# MM
		# size = 144456
		#
		# examples: A81AB0A616889CC2

		# RCRA
		# size = 96984
		#
		# examples: A81AB0A616889CC2
		
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
		return "7F9A96AA ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 7F9A96AA     | {:6} entries".format(self.TAG, len(self.entries)))

