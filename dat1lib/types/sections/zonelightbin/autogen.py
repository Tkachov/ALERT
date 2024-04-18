# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

#

class x101A2196_Section(dat1lib.types.sections.Section):
	TAG = 0x101A2196
	TYPE = 'ZoneLightBin'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 3496 occurrences in 3496 files (always present)
		# size = 8
		# always last
		#
		# examples: 80033BFC093E747C

		# RCRA
		# 648 occurrences in 648 files (always present)
		# size = 8
		#
		# examples: 8009BEE1DCEA1DEE
		
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
		return "101A2196 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 101A2196     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x27204B67_Section(dat1lib.types.sections.Section):
	TAG = 0x27204B67
	TYPE = 'ZoneLightBin'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 3496 occurrences in 3496 files (always present)
		# size = 12..11952 (avg = 3461.2)
		# always first
		#
		# examples: 850FB496E7E729A7 (min size), 86541177E5784288 (max size)

		# RCRA
		# 648 occurrences in 648 files (always present)
		# size = 12..124944 (avg = 6128.5)
		# always first
		#
		# examples: 807DAB2AE0537D30 (min size), 943164D491D45E13 (max size)
		
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
		return "27204B67 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 27204B67     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xC72A514C_Section(dat1lib.types.sections.Section):
	TAG = 0xC72A514C
	TYPE = 'ZoneLightBinRcra'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: none

		# RCRA
		# 35 occurrences in 648 files
		# size = 8..41652 (avg = 5527.3)
		#
		# examples: A453C793F7C9E21F (min size), 943164D491D45E13 (max size)
		
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
		return "C72A514C ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | C72A514C     | {:6} entries".format(self.TAG, len(self.entries)))
