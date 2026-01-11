# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib
import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class AssetHeader(object):
	def __init__(self, f, header_size):
		data = f.read(header_size)
		count = len(data) // 4
		values = struct.unpack("<" + "I" * count, data)
		self.magic = values[0] if count > 0 else 0
		self.values = list(values[1:]) if count > 1 else []

	def save(self, f):
		f.write(struct.pack("<I", self.magic))
		for value in self.values:
			f.write(struct.pack("<I", value))

#

STG_FLAGS_INSTALL_HEADER = 1
STG_FLAGS_INSTALL_TEXTURE_META = 2

class STG(object):
	STG_MAGIC = 0x475453 # STG

	def __init__(self, f):
		magic_and_version, flags, header_size, texture_meta_size = struct.unpack("<IIII", f.read(16))
		self.magic = magic_and_version & 0xFFFFFF
		self.version = (magic_and_version >> 24) & 0xFF
		self.flags = flags

		if self.magic != self.STG_MAGIC:
			print(f"[!] Bad STG magic: {self.magic:06X} (isn't equal to expected {self.STG_MAGIC:06X})")

		if self.version != 0:
			print(f"[!] Unknown STG version: {self.version}")

		self.header = AssetHeader(f, header_size)
		utils.read_to_align(f, 16)

		self.texture_meta = f.read(texture_meta_size)
		utils.read_to_align(f, 16)
		
		data = f.read()
		self.dat1 = dat1lib.read_dat1(io.BytesIO(data))

	@classmethod
	def make(cls):
		data = struct.pack("<IIII", cls.STG_MAGIC, 0, 8, 0)
		data += struct.pack("<IBBH", 0, 0, 0, 0)
		data += struct.pack("<II", 0, 0) # padding to 16
		data += dat1lib.types.dat1.DAT1.EMPTY_DATA
		return cls(io.BytesIO(data))

	def save(self, f):
		of = io.BytesIO(bytes())
		self.header.save(of)
		of.seek(0)
		header = of.read()

		magic_and_version = (self.magic & 0xFFFFFF) | ((self.version & 0xFF) << 24)
		f.write(struct.pack("<IIII", magic_and_version, self.flags, len(header), len(self.texture_meta)))

		f.write(header)
		utils.write_to_align(f, 16)

		f.write(self.texture_meta)
		utils.write_to_align(f, 16)

		self.dat1.save(f)

	def has_texture_meta(self):
		return len(self.texture_meta) > 0
