# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

#

class x5DA317BF_Section(dat1lib.types.sections.Section):
	TAG = 0x5DA317BF
	TYPE = 'Material_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5821 occurrences in 6925 files
		# size = 16..864 (avg = 147.7)
		#
		# examples: 01AF2AD7 (min size), 6254DEE0 (max size)

		# similar to A59F667B, but SO/Material-specific (A5... is only MaterialGraph in SO and both Material/MaterialGraph in MSMR)
		
		self.data = data

	def save(self):
		of = io.BytesIO(bytes())
		of.write(self.data)
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "5DA317BF ({} bytes)".format(len(self.data))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 5DA317BF     | {:6} bytes".format(self.TAG, len(self.data)))

	def web_repr(self):
		return {"name": "5DA317BF", "type": "text", "readonly": True, "content": "{} bytes\n(see F2DC60EC for displayed values)\n\n".format(len(self.data))}

#

class xB967FF7A_Section(dat1lib.types.sections.Section):
	TAG = 0xB967FF7A
	TYPE = 'Material_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 6206 occurrences in 6925 files
		# size = 16..640 (avg = 162.1)
		#
		# examples: 045B0C66 (min size), 5E0A1CAD (max size)

		# similar to 1CAFE804, but SO/Material-specific (1C... is only MaterialGraph in SO and both Material/MaterialGraph in MSMR)
		
		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<IHHII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<IHHII", *e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "B967FF7A ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | B967FF7A     | {:6} entries".format(self.TAG, len(self.entries)))

		print()
		#######........ | 123  123456  123456  12345678  12345678  ...
		print("           #    ?       index?  slot?     type?     texture")
		print("         ----------------------------------------------------")
		for i in range(len(self.entries)):
			spos, a, b, c, d = self.entries[i]
			s = self._dat1.get_string(spos)
			if s is None:
				s = "<str at {}>".format(spos)

			print("         - {:<3}  {:<6}  {:<6}  {:08X}  {:08X}  {}".format(i, a, b, c, d, repr(s)))
		print()

#

class xBDC72826_Section(dat1lib.types.sections.Section):
	TAG = 0xBDC72826
	TYPE = 'Material_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 6779 occurrences in 6925 files
		# size = 12..24 (avg = 23.5)
		#
		# examples: 01AF2AD7 (min size), 000C8FCD (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "BDC72826 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | BDC72826     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xF2DC60EC_Section(dat1lib.types.sections.Section):
	TAG = 0xF2DC60EC
	TYPE = 'Material_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5822 occurrences in 6925 files
		# size = 8..1376 (avg = 187.3)
		#
		# examples: 0524FA2B (min size), 6254DEE0 (max size)

		# similar to 45C4F4C0, but SO/Material-specific (45... is only MaterialGraph in SO and both Material/MaterialGraph in MSMR)
		
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<HHI", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<HHI", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "F2DC60EC ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | F2DC60EC     | {:6} parameters".format(self.TAG, len(self.entries)))

		data_section = self._dat1.get_section(0x5DA317BF)
		data = data_section._raw

		for i, e in enumerate(self.entries):
			offset, size, code = e
			print(f" - {i:<3} {code:08X} = " + (" ".join([f"{x:02X}" for x in data[offset:offset+size]])))
