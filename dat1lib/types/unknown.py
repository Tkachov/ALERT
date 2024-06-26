# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

# .movie = BIK
# .zonelightbin = strange 1TAD/asset, 38 bytes asset header instead of 36

class UnknownAsset(object):
	def __init__(self, f, version=None):
		self.version = version

		self.magic, self.likely_is_dat1_size = struct.unpack("<II", f.read(8))
		self.unk = f.read(28)
		self._raw_dat1 = f.read()

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def print_info(self, config):
		print("-------")
		print("Asset? {:08X}".format(self.magic))
		print("- size?  = {}".format(self.likely_is_dat1_size))
		utils.print_bytes_formatted(self.unk, "- ", 2)
		print("-------")
		print("")

		self.dat1.print_info(config)
