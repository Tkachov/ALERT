import dat1lib.types.sections
import dat1lib.types.sections.model.geo
import io
import struct
import dat1lib.float16 as f16

#

class x16F3BA18_Section(dat1lib.types.sections.Section):
	TAG = 0x16F3BA18
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 8775 occurrences in 8780 files
		# size = 12..2213544 (avg = 16140.1)
		#
		# examples: 2AD6B126 (min size), 7929FC02 (max size)

		self.data = data
		self.f16 = None

	def save(self):
		of = io.BytesIO(bytes())
		of.write(self.data)
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "16F3BA18 ({} bytes)".format(len(self.data))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 16F3BA18     | {:6} bytes".format(self.TAG, len(self.data)))

	def get_uv(self, vertex_index):
		s = self._dat1.get_section(dat1lib.types.sections.model.geo.VertexesSection.TAG)
		sz = len(s._raw) // 16

		ENTRY_SIZE = 4
		if sz*8 == len(self.data):
			ENTRY_SIZE = 8

		u, v = None, None
		if ENTRY_SIZE == 4:
			u, v = struct.unpack("<hh", self.data[vertex_index*ENTRY_SIZE:(vertex_index+1)*ENTRY_SIZE])
			u = self._unpack(u)
			v = self._unpack(v)
		else:
			u, v, _, _ = struct.unpack("<hhhh", self.data[vertex_index*ENTRY_SIZE:(vertex_index+1)*ENTRY_SIZE])
			u = self._unpack(u)
			v = self._unpack(v)
			# TODO: what is the second pair for?
			# 	maybe that's multiple UV layers?
			# 	in that case, maybe it's possible that there is more than 2, so not only 4 and 8 cases must be handled here?

		return (u, v)

	def _unpack(self, packed_f16):
		if self.f16 is None:
			self.f16 = f16.Float16Compressor()

		return self.f16.decompress_and_unpack(packed_f16)

#

class x237D59F1_Section(dat1lib.types.sections.Section):
	TAG = 0x237D59F1
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 9 occurrences in 8780 files
		# size = 160..12314 (avg = 1888.4)
		#
		# examples: 4FE34225 (min size), 7927C845 (max size)
		pass

	def get_short_suffix(self):
		return "237D59F1 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 237D59F1     | {:6} bytes".format(self.TAG, len(self._raw)))

#

class x5796FEF6_Section(dat1lib.types.sections.Section):
	TAG = 0x5796FEF6
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5166 occurrences in 8780 files
		# size = 10..384190 (avg = 4249.8)
		#
		# examples: 36F6496B (min size), 7929FC02 (max size)
		pass

	def get_short_suffix(self):
		return "5796FEF6 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 5796FEF6     | {:6} bytes".format(self.TAG, len(self._raw)))

#

class x4AD86765_Section(dat1lib.types.sections.Section):
	TAG = 0x4AD86765
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3508 occurrences in 8780 files
		# size = 16..2848 (avg = 254.4)
		#
		# examples: 0078706C (min size), 7E3E18BC (max size)
		
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
		return "4AD86765 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 4AD86765     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x45079BC5_Section(dat1lib.types.sections.Section):
	TAG = 0x45079BC5
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 9 occurrences in 8780 files
		# size = 27888..7305120 (avg = 1185632.0)
		#
		# examples: 4FE34225 (min size), 7927C845 (max size)
		
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
		return "45079BC5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 45079BC5     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xF4CB2F37_Section(dat1lib.types.sections.Section):
	TAG = 0xF4CB2F37
	TYPE = 'Model_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5166 occurrences in 8780 files
		# size = 18..235590 (avg = 1664.7)
		#
		# examples: 36F6496B (min size), 7929FC02 (max size)
		pass

	def get_short_suffix(self):
		return "F4CB2F37 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | F4CB2F37     | {:6} bytes".format(self.TAG, len(self._raw)))
