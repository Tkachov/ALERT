# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

class TextureHeaderSection(dat1lib.types.sections.Section):
	TAG = 0x62297090 # Archive TOC Texture Header

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)
		self.count = struct.unpack("<I", data)[0]

	def save(self):
		return struct.pack("<I", self.count)

#

class TextureAssetIdsSection(dat1lib.types.sections.Section):
	TAG = 0x36A6C8CC # Archive TOC Texture Asset Ids

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.ids = [struct.unpack("<Q", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for aid in self.ids:
			of.write(struct.pack("<Q", aid))
		of.seek(0)
		return bytearray(of.read())

#

class TextureMetaSection(dat1lib.types.sections.Section):
	TAG = 0xC9FB9DDA # Archive TOC Texture Meta
	META_SIZE = 72

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)
		self.buffer = data

	def save(self):
		return self.buffer

	def get_texture_meta(self, texture_index):
		return self.buffer[self.META_SIZE * texture_index:self.META_SIZE * (texture_index + 1)]
