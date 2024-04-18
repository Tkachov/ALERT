# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

#

class TextureHeaderSection(dat1lib.types.sections.Section):
	TAG = 0x4EDE3593
	TYPE = 'Texture'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 42840 occurrences in 42840 files (always present)
		# size = 36
		# always first
		# always last
		#
		# examples: 0001E8B9

		# MSMR
		# 25602 occurrences in 25602 files (always present)
		# size = 44
		# always first
		# always last
		#
		# examples: 800035F1EBDCBCEC

		# MM
		# 20652 occurrences in 20652 files (always present)
		# size = 44
		# always first
		# always last
		#
		# examples: 800035F1EBDCBCEC

		# RCRA
		# 12502 occurrences in 12502 files (always present)
		# size = 44
		# always first
		# always last
		#
		# examples: 8001D626C025EAA0

		# named according to https://github.com/monax3/SpiderTex/blob/main/src/texture_file.rs

		self.sd_len, self.hd_len = struct.unpack("<II", data[:8])
		self.hd_width, self.hd_height = struct.unpack("<HH", data[8:12])
		self.sd_width, self.sd_height = struct.unpack("<HH", data[12:16])
		self.array_size, self.stex_format, self.planes = struct.unpack("<HBB", data[16:20])
		if self.version == dat1lib.VERSION_SO:
			self.fmt, _, _, self.sd_mipmaps, self.unk2 = struct.unpack("<HHIBB", data[20:30])
			self.unk, self.unk3, self.hd_mipmaps = struct.unpack("<IBB", data[30:36])
			self.unk4 = data[36:]
		else:
			self.fmt, self.unk = struct.unpack("<HQ", data[20:30])
			self.sd_mipmaps, self.unk2, self.hd_mipmaps, self.unk3 = struct.unpack("<BBBB", data[30:34])
			self.unk4 = data[34:]

	def save(self):
		of = io.BytesIO(bytes())
		of.write(struct.pack("<II", self.sd_len, self.hd_len))
		of.write(struct.pack("<HH", self.hd_width, self.hd_height))
		of.write(struct.pack("<HH", self.sd_width, self.sd_height))
		of.write(struct.pack("<HBB", self.array_size, self.stex_format, self.planes))
		of.write(struct.pack("<HQ", self.fmt, self.unk))
		of.write(struct.pack("<BBBB", self.sd_mipmaps, self.unk2, self.hd_mipmaps, self.unk3))
		of.write(self.unk4)
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "texture header"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | tex. header  |".format(self.TAG))
		print("\tSD len={}, {}x{}, {} mipmaps".format(self.sd_len, self.sd_width, self.sd_height, self.sd_mipmaps))
		print("\tHD len={}, {}x{}, {} mipmaps".format(self.hd_len, self.hd_width, self.hd_height, self.hd_mipmaps))
		print("\tarray_size={}, stex_format={}, planes={}, format={}".format(self.array_size, self.stex_format, self.planes, self.fmt))
		print("\t{:016X} {:02X} {:02X} {}".format(self.unk, self.unk2, self.unk3, "".join(["{:02X}".format(c) for c in self.unk4])))
		print("")
