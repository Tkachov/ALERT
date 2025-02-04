# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

class HeaderSection(dat1lib.types.sections.Section):
	TAG = 0x4765351A # Sound Bank Built

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.a, self.b, self.bnk_section_size = struct.unpack("<HHI", data[:8])
		rest = data[8:]

		ENTRY_SIZE = 4
		count = len(rest)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", rest[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		
		of.write(struct.pack("<HHI", self.a, self.b, self.bnk_section_size))
		for e in self.entries:
			of.write(struct.pack("<I", e))
		
		of.seek(0)
		return of.read()
