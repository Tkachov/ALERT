# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.crc32 as crc32
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class HeaderSection(dat1lib.types.sections.Section):
	TAG = 0x4765351A # Sound Bank Built
	TYPE = 'soundbank'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 1473 occurrences in 1473 files (always present)
		# size = 64
		# always first
		#
		# examples: 010FB3C2

		# MSMR
		# 1345 occurrences in 1345 files (always present)
		# size = 64
		# always first
		#
		# examples: 801825F7A321A714

		# MM
		# 1239 occurrences in 1239 files (always present)
		# size = 64
		# always first
		#
		# examples: 800BAAC604A8B370

		# RCRA
		# 1218 occurrences in 1218 files (always present)
		# size = 64
		# always first
		#
		# examples: 800582AB4AE61DB1

		self.a, self.b, self.bnk_section_size = struct.unpack("<HHI", data[:8])
		rest = data[8:]

		ENTRY_SIZE = 4
		count = len(rest)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", rest[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def get_short_suffix(self):
		return "header"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Header       |".format(self.TAG))
		print(" "*11 + "{}  {}  {}".format(self.a, self.b, self.bnk_section_size))
		print(" "*11 + " ".join(["{}".format(x) for x in self.entries]))
		print("")

	def web_repr(self):
		content = ""
		content += "    a: {}\n".format(self.a)
		content += "    b: {}\n".format(self.b)
		content += " size: {}\n".format(self.bnk_section_size)
		content += " rest: " + " ".join([f"{x}" for x in self.entries])
		content += "\n"		
		return {"name": "Header", "type": "text", "readonly": True, "content": content}
