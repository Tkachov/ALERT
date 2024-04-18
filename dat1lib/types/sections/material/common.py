# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

# common with .materialgraph

class x1CAFE804_Section(dat1lib.types.sections.Section):
	TAG = 0x1CAFE804
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 950 occurrences in 1012 files
		# met only in MaterialGraph
		# size = 16..608 (avg = 100.9)
		#
		# examples: 08B1979D (min size), 3E35F844 (max size)

		# MSMR
		# 4423 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 16..432 (avg = 130.3)
		#
		# examples: 8000E61F841EBC5F (min size), 833688BC03CD8BAB (max size)

		# MM
		# 4473 occurrences in 1157 files
		# met in Material, MaterialGraph
		# size = 16..432 (avg = 171.8)
		#
		# examples: 8000E61F841EBC5F (min size), 9D7D20AA12DFABFA (max size)

		# RCRA
		# 2494 occurrences in 1474 files
		# met in Material, MaterialGraph
		# size = 16..416 (avg = 94.1)
		#
		# examples: 8002FF0468195E56 (min size), 9D50E3692BED4B20 (max size)
		
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
		return "1CAFE804 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 1CAFE804     | {:6} entries".format(self.TAG, len(self.entries)))

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

class x45C4F4C0_Section(dat1lib.types.sections.Section):
	TAG = 0x45C4F4C0
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 846 occurrences in 1012 files
		# met only in MaterialGraph
		# size = 8..672 (avg = 115.3)
		#
		# examples: 1BDC5883 (min size), 5DBE1A14 (max size)

		# MSMR
		# 4389 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 8..536 (avg = 167.0)
		#
		# examples: 81FB726316B0A0CA (min size), 83D5CEEBCD8A4609 (max size)

		# MM
		# 4381 occurrences in 1157 files
		# met in Material, MaterialGraph
		# size = 8..568 (avg = 217.6)
		#
		# examples: 80622C8227472B8A (min size), 80993366A7C61A94 (max size)

		# RCRA
		# 2446 occurrences in 1474 files
		# met in Material, MaterialGraph
		# size = 8..776 (avg = 155.7)
		#
		# examples: 800CF5F75DDEBDE0 (min size), 9D055F3435E7D244 (max size)

		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.params_keys = [struct.unpack("<HHI", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.params_keys:
			of.write(struct.pack("<HHI", *e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "45C4F4C0 ({})".format(len(self.params_keys))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 45C4F4C0     | {:6} parameters".format(self.TAG, len(self.params_keys)))

		s = self._dat1.get_section(0xA59F667B)
		params_values = s.data

		params = []
		for offset, size, key in self.params_keys:
			params += [(key, params_values[offset:offset+size])]

		print()
		#######........ | 123  12345678  ...
		print("           #    slotname  value")
		print("         -----------------------------")
		for i, (k, v) in enumerate(params):
			print("         - {:<3}  {:08X}  {}".format(i, k, utils.format_bytes(v)))
		print()

#

class xA59F667B_Section(dat1lib.types.sections.Section):
	TAG = 0xA59F667B
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 846 occurrences in 1012 files
		# met only in MaterialGraph
		# size = 16..416 (avg = 85.6)
		#
		# examples: 02670F45 (min size), 3E35F844 (max size)

		# MSMR
		# 4389 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 16..352 (avg = 125.8)
		#
		# examples: 8000E61F841EBC5F (min size), 9FC1F81BF116DE2B (max size)

		# MM
		# 4381 occurrences in 1157 files
		# met in Material, MaterialGraph
		# size = 16..368 (avg = 152.5)
		#
		# examples: 8000E61F841EBC5F (min size), 815C70A0EAFA956C (max size)

		# RCRA
		# 2446 occurrences in 1474 files
		# met in Material, MaterialGraph
		# size = 16..416 (avg = 104.7)
		#
		# examples: 800CF5F75DDEBDE0 (min size), 9D055F3435E7D244 (max size)
		
		self.data = data

	def save(self):
		of = io.BytesIO(bytes())
		of.write(self.data)
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "A59F667B ({} bytes)".format(len(self.data))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | A59F667B     | {:6} bytes".format(self.TAG, len(self.data)))

	def web_repr(self):
		return {"name": "A59F667B", "type": "text", "readonly": True, "content": "{} bytes\n(see 45C4F4C0 for displayed values)\n\n".format(len(self.data))}

#

class x8C049CCA_Section(dat1lib.types.sections.Section):
	TAG = 0x8C049CCA
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 4530 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 400..800 (avg = 523.5)
		#
		# examples: 800BAF6EA093111C (min size), 8000E61F841EBC5F (max size)

		# MM
		# 4586 occurrences in 1157 files
		# met in Material, MaterialGraph
		# size = 400..800 (avg = 569.1)
		#
		# examples: 800BAF6EA093111C (min size), 8000E61F841EBC5F (max size)

		# RCRA
		# 2639 occurrences in 1474 files
		# met in Material, MaterialGraph
		# size = 288..576 (avg = 321.5)
		#
		# examples: 8002A246A1293FB6 (min size), 800809D3288F5C7E (max size)
		
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
		return "8C049CCA ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 8C049CCA     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xBBFC8900_Section(dat1lib.types.sections.Section):
	TAG = 0xBBFC8900
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 4530 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 180352..1088640 (avg = 539245.6)
		#
		# examples: A8FE8763415A6F99 (min size), 8E1F4B600684B170 (max size)

		# MM
		# 4586 occurrences in 1157 files
		# met in Material, MaterialGraph
		# size = 178368..1334760 (avg = 617902.3)
		#
		# examples: A315153F6A2EA5F2 (min size), 9C59C707EF49E793 (max size)

		# RCRA
		# 2639 occurrences in 1474 files
		# met in Material, MaterialGraph
		# size = 95744..1112524 (avg = 396042.1)
		#
		# examples: A8A61DE9B77F351F (min size), 809D690CEE3F6048 (max size)
		
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
		return "BBFC8900 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | BBFC8900     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xBC93FB5E_Section(dat1lib.types.sections.Section):
	TAG = 0xBC93FB5E
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 1012 occurrences in 1012 files (always present)
		# met only in MaterialGraph
		# size = 20..40 (avg = 38.9)
		#
		# examples: 02670F45 (min size), 007C5193 (max size)

		# MSMR
		# 4530 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 280..560 (avg = 366.4)
		#
		# examples: 800BAF6EA093111C (min size), 8000E61F841EBC5F (max size)

		# MM
		# 4586 occurrences in 1157 files
		# met in Material, MaterialGraph
		# size = 280..560 (avg = 398.3)
		#
		# examples: 800BAF6EA093111C (min size), 8000E61F841EBC5F (max size)

		# RCRA
		# 2639 occurrences in 1474 files
		# met in Material, MaterialGraph
		# size = 280..560 (avg = 312.5)
		#
		# examples: 8002A246A1293FB6 (min size), 800809D3288F5C7E (max size)
		
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
		return "BC93FB5E ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | BC93FB5E     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xC24B19D9_Section(dat1lib.types.sections.Section):
	TAG = 0xC24B19D9
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# met only in MaterialGraph
		# size = 16
		#
		# examples: 7376D96B

		# MSMR
		# 279 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 8..16 (avg = 9.1)
		#
		# examples: 8037745A90D97633 (min size), 81314739879CD24C (max size)

		# MM
		# 438 occurrences in 1157 files
		# met in Material, MaterialGraph
		# size = 8..32 (avg = 11.3)
		#
		# examples: 8061D72FD2A04308 (min size), 8516DFCD8E10CAB6 (max size)

		# RCRA
		# 84 occurrences in 1474 files
		# met in Material, MaterialGraph
		# size = 8..24 (avg = 9.0)
		#
		# examples: 8094C0D290CEA302 (min size), 8BCD795B587E7DBF (max size)
		
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
		return "C24B19D9 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | C24B19D9     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xF9C35F30_Section(dat1lib.types.sections.Section):
	TAG = 0xF9C35F30
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2818 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 20
		#
		# examples: 800BAF6EA093111C

		# MM
		# 2905 occurrences in 1157 files
		# met in Material, MaterialGraph
		# size = 20
		#
		# examples: 800BAF6EA093111C

		# RCRA
		# 1167 occurrences in 1474 files
		# met in Material, MaterialGraph
		# size = 16
		#
		# examples: 8002A246A1293FB6
		
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
		return "F9C35F30 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | F9C35F30     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xFD113362_Section(dat1lib.types.sections.Section):
	TAG = 0xFD113362
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 1751 occurrences in 1049 files
		# met in Material, MaterialGraph
		# size = 8
		#
		# examples: 800BAF6EA093111C

		# MM
		# 1297 occurrences in 1157 files
		# met in Material, MaterialGraph
		# size = 8
		#
		# examples: 800BAF6EA093111C

		# RCRA
		# 198 occurrences in 1474 files
		# met in Material, MaterialGraph
		# size = 8
		#
		# examples: 8082DC3324651BC5
		
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
		return "FD113362 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | FD113362     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xC32E7230_Section(dat1lib.types.sections.Section):
	TAG = 0xC32E7230
	TYPE = 'Material/MaterialGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: none

		# MM
		# 11 occurrences in 1157 files
		# met in Material, MaterialGraph
		# size = 4
		#
		# examples: 8516DFCD8E10CAB6

		# RCRA
		# 3 occurrences in 1474 files
		# met in MaterialGraph only
		# size = 4..8 (avg = 6.6)
		#
		# examples: 88DD264D68FD252A (min size), 80CF3B386B06DF44 (max size)
		
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
		return "C32E7230 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | C32E7230     | {:6} entries".format(self.TAG, len(self.entries)))
