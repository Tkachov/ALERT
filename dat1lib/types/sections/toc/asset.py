# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

class AssetIdsSection(dat1lib.types.sections.Section):
	TAG = 0x506D7B8A # Archive TOC Asset IDs

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

class AssetMetadata(object):
	def __init__(self, data):
		self.size, self.archive_index, self.offset, self.header_offset = struct.unpack("<IIIi", data)

	def save(self, of):
		of.write(struct.pack("<IIIi", self.size, self.archive_index, self.offset, self.header_offset))

class AssetMetadataSection(dat1lib.types.sections.Section):
	TAG = 0x65BCF461 # Archive TOC Asset Metadata

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.entries = [AssetMetadata(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			e.save(of)
		of.seek(0)
		return bytearray(of.read())

#

class AssetHeaderDataSection(dat1lib.types.sections.Section):
	TAG = 0x654BDED9 # Archive TOC Asset Header Data

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)
		self.buffer = data

	def save(self):
		return self.buffer

	def read_header(self, offset):
		_, pairs, extra = struct.unpack("<BBH", self.buffer[offset+4:offset+8])
		total_size = 8 + pairs * 8 + extra
		return self.buffer[offset:offset+total_size]			
