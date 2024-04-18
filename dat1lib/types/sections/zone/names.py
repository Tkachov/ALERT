# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

class ZoneActorNamesSection(dat1lib.types.sections.Section):
	TAG = 0xDC625B3D # Zone Actor Names
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 1767 occurrences in 4936 files
		# size = 4..1696 (avg = 136.6)
		#
		# examples: 001D706D (min size), 8EDC1A61 (max size)

		# MSMR
		# 6510 occurrences in 12274 files
		# size = 4..53416 (avg = 177.0)
		#
		# examples: 800718BAACC0D46B (min size), 9419A66DCDCE388E (max size)

		# MM
		# 5019 occurrences in 10473 files
		# size = 4..53576 (avg = 179.3)
		#
		# examples: 80284FCAF03DFDFF (min size), 9419A66DCDCE388E (max size)

		# RCRA
		# 1599 occurrences in 9046 files
		# size = 4..35104 (avg = 176.7)
		#
		# examples: 8064BAF4CDF6C8C2 (min size), 8683FD7F7ABDC494 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.names = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.names:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Zone Actor Names ({})".format(len(self.names))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Actor Names  | {:6} names".format(self.TAG, len(self.names)))
		for i, x in enumerate(self.names):
			print("  - {:<3}  {}".format(i, self._dat1.get_string(x)))
		print("")
