# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

class ArchiveFileEntry(object):
	def __init__(self, data):
		self.filename = data[:40]
		self.a, self.b, self.c, self.d, self.e = struct.unpack("<QQIHI", data[40:])

	def save(self, of):		
		of.write(self.filename)
		of.write(struct.pack("<QQIHI", self.a, self.b, self.c, self.d, self.e))

	def get_filename(self):
		fn = self.filename

		i = fn.index(b'\0')
		if i != -1:
			fn = fn[:i]
		fn = fn.decode('ascii')

		return fn

	def set_filename(self, filename):
		f = io.BytesIO()
		f.write(filename.encode('ascii'))
		LN = 40
		if len(filename) < LN:
			f.write(b'\0' * (LN - len(filename)))
		f.seek(0)

		self.filename = f.read()

class FileMetadataSection(dat1lib.types.sections.Section):
	TAG = 0x398ABFF0 # Archive TOC File Metadata

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 66
		count = len(data)//ENTRY_SIZE
		self.archives = [ArchiveFileEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.archives:
			e.save(of)
		of.seek(0)
		return bytearray(of.read())
