# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.stg
import io

class Model(dat1lib.types.stg.STG):
	MAGIC = 0x9D2C0FA9

	def __init__(self, f):
		dat1lib.types.stg.STG.__init__(self, f)

		if self.header.magic != self.MAGIC:
			print(f"[!] Bad Model magic: {self.header.magic:08X} (isn't equal to expected {self.MAGIC:08X})")

	def save(self, f):
		# Find offset to section 0x0859863D (IndexesSection)
		offset_to_indexbuf = 0
		for s in self.dat1.header.sections:
			if s.tag == 0x0859863D:
				offset_to_indexbuf = s.offset
				break
		
		# Ensure header has at least one value and update it
		if len(self.header.values) == 0:
			self.header.values.append(0)
		self.header.values[0] = offset_to_indexbuf

		dat1lib.types.stg.STG.save(self, f)
