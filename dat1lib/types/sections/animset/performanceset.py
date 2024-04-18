# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.crc32 as crc32
import dat1lib.types.sections
import io
import struct

class ClipsListSection(dat1lib.types.sections.Section):
	TAG = 0xC8CE8D96
	TYPE = 'performanceset'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 320 occurrences in 320 .performanceset files
		# size = 24..253032 (avg = 3152.7)
		#
		# examples: 81C13ECB778F64AD (min size), 9B4C33CE8CA86160 (max size)

		# MM
		# 108 occurrences in 953 files
		# size = 24..139560 (avg = 5060.2)
		#
		# examples: A5A17E16E08C3011 (min size), 924A892B91713303 (max size)

		# RCRA
		# 107 occurrences in 787 files
		# size = 24..39816 (avg = 3225.8)
		#
		# examples: 808FDC29C34278A6 (min size), A701A4EED5E40B44 (max size)
		
		ENTRY_SIZE = 24
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<IIQQ", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]
		# sorted by e[0]
		# e[1] mostly 0, but can be crc32-like
		# e[2] .performanceclip asset_id
		# e[3] .animclip asset_id

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<IIQQ", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "clips list ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Clips List   | {:6} .performanceclips".format(self.TAG, len(self.entries)))

		##### "  - 123  12345678 12345678 1234567812345678 1234567812345678
		print("      #         ?        ? .performanceclip        .animclip")
		print("  ----------------------------------------------------------")
		for i, x in enumerate(self.entries):
			print("  - {:<3}  {:08X} {:08X} {:016X} {:016X}".format(i, *x))
		print("")
