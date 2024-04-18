# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

class SkinBatch(object):
	ENTRY_SIZE = 16

	def __init__(self):
		self.offset = 0
		self.z1 = 0
		self.z2 = 0
		self.unk1 = 0
		self.vertex_count = 0
		self.first_vertex = 0

	@classmethod
	def make(cls, data):
		b = cls()
		b.load(data)
		return b

	def load(self, data):
		self.offset, self.z1, self.z2, self.unk1, self.vertex_count, self.first_vertex = struct.unpack("<IIHHHH", data)

	def save(self):
		return struct.pack("<IIHHHH", self.offset, self.z1, self.z2, self.unk1, self.vertex_count, self.first_vertex)

class ModelSkinBatchSection(dat1lib.types.sections.Section):
	TAG = 0xC61B1FF5 # Model Skin Batch
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 3470 occurrences in 8780 files
		# size = 16..4848 (avg = 204.3)
		#
		# examples: 0078706C (min size), 7E3E18BC (max size)

		# MSMR
		# 2121 occurrences in 38298 files
		# size = 16..16256 (avg = 453.0)
		#
		# examples: 800C84622E8A0075 (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 1688 occurrences in 37147 files
		# size = 16..10656 (avg = 408.0)
		#
		# examples: 800C84622E8A0075 (min size), AD7386F5F9A76C43 (max size)

		# RCRA
		# 959 occurrences in 11387 files
		# size = 16..24432 (avg = 1069.2)
		#
		# examples: 80E4E1B6E9D6B81A (min size), A428F4A59DA18D74 (max size)

		count = len(data) // SkinBatch.ENTRY_SIZE
		self.batches = [SkinBatch.make(data[i*SkinBatch.ENTRY_SIZE:(i+1)*SkinBatch.ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for b in self.batches:
			of.write(b.save())
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Model Skin Batch ({})".format(len(self.batches))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Skin Batch   | {:6} structs".format(self.TAG, len(self.batches)))

		print()
		#######........ | 123  12345678  1234  1234  12345678  12345678  12345678
		print("           #      offset     0     0         ?  vrtx cnt  vrtx off")
		print("         -----------------------------------------------------------------")
		for i, l in enumerate(self.batches):
			print("         - {:<3}  {:8}  {:4}  {:4}  {:8}  {:8}  {:8}".format(i, l[0], l[1], l[2], l[3], l[4], l[5]))
		print()

#

class ModelSkinDataSection(dat1lib.types.sections.Section): # vertex weights
	TAG = 0xDCA379A2 # Model Skin Data
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 3470 occurrences in 8780 files
		# size = 4..845968 (avg = 31616.6)
		#
		# examples: 1254B70A (min size), EED9B1B8 (max size)

		# MSMR
		# 2121 occurrences in 38298 files
		# size = 5..5642457 (avg = 157231.4)
		#
		# examples: 8D8CB10A938FE720 (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 1688 occurrences in 37147 files
		# size = 5..4446860 (avg = 122931.2)
		#
		# examples: A83AC87DC5553DBC (min size), 8DDE07945B10DDB3 (max size)

		# RCRA
		# 959 occurrences in 11387 files
		# size = 5..7348561 (avg = 249085.2)
		#
		# examples: 8B4C8E19832AE134 (min size), 988A53437037246E (max size)
		pass

	def save(self):
		of = io.BytesIO(bytes())
		of.write(self._raw)
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "Model Skin Data ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return

		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Skin Data    | {:6} bytes".format(self.TAG, len(self._raw)))

	def web_repr(self):
		return {"name": "Model Skin Data", "type": "text", "readonly": True, "content": "{} bytes".format(len(self._raw))}

#

class xCCBAFF15_Section(dat1lib.types.sections.Section):
	TAG = 0xCCBAFF15
	TYPE = 'Model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: none
		# MM: none

		# RCRA
		# 954 occurrences in 11387 files
		# size = 32..21394920 (avg = 789337.3)
		#
		# examples: 8B4C8E19832AE134 (min size), AE2DF2353798682F (max size)
		
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<8B", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]
		# <bone><bone><bone><bone>
		# <weight><weight><weight><weight>

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<8B", *e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "RCRA weights ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | RCRA weights | {:6} entries".format(self.TAG, len(self.entries)))

	def web_repr(self):
		return {"name": "RCRA weights", "type": "text", "readonly": True, "content": f"{len(self.entries)} weights"}
