# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.stg
import dat1lib.types.sections.soundbank.bnk
import dat1lib.types.sections.soundbank.header
import dat1lib.types.sections.soundbank.info
import dat1lib.types.sections.soundbank.strings
import io

class Soundbank(dat1lib.types.stg.STG):
	MAGIC = 0x66350FBB

	def __init__(self, f):
		dat1lib.types.stg.STG.__init__(self, f)

		if self.header.magic != self.MAGIC:
			print(f"[!] Bad Soundbank magic: {self.header.magic:08X} (isn't equal to expected {self.MAGIC:08X})")

	def save(self, f):
		of = io.BytesIO(bytes())
		self.dat1.save(of)
		of.seek(0)
		dat1_data = of.read()

		_, b = self.header.pairs[0]
		self.header.pairs[0] = (len(dat1_data) | 0x40000000, b)

		dat1lib.types.stg.STG.save(self, f)

	#

	def get_header_section(self):
		return self.dat1.get_section(dat1lib.types.sections.soundbank.header.HeaderSection.TAG)

	def get_strings_section(self):
		return self.dat1.get_section(dat1lib.types.sections.soundbank.strings.StringsSection.TAG)

	def get_info_section(self):
		return self.dat1.get_section(dat1lib.types.sections.soundbank.info.InfoSection.TAG)

	def get_wwise_bank_section(self):
		return self.dat1.get_section(dat1lib.types.sections.soundbank.bnk.WwiseBankSection.TAG)

	#

	def replace_wwise_bank_section(self, new_data):
		BNK_SECTION = dat1lib.types.sections.soundbank.bnk.WwiseBankSection.TAG
		self.dat1.get_section(BNK_SECTION).replace_data(new_data)
		self.dat1.refresh_section_data(BNK_SECTION)

		HEADER_SECTION = dat1lib.types.sections.soundbank.header.HeaderSection.TAG
		self.dat1.get_section(HEADER_SECTION).bnk_section_size = len(new_data)
		self.dat1.refresh_section_data(HEADER_SECTION)
