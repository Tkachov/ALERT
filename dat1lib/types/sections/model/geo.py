import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class IndexesSection(dat1lib.types.sections.Section): # aka model_index
	TAG = 0x0859863D
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 38298 occurrences in 38298 files (always present)
		# size = 6..10127496 (avg = 21726.4)
		#
		# examples: 803D66A8B5147C41 (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 37144 occurrences in 37147 files
		# size = 6..4706040 (avg = 15410.0)
		#
		# examples: 83C4C8562CDC453B (min size), 90B61AD0494B91C9 (max size)

		self._delta_encoded = utils.read_struct_N_array_data(data, len(data)//2, "<h")
		self.values = []

		if len(self._delta_encoded) > 0:
			self.values += [self._delta_encoded[0]]

		for i in range(1, len(self._delta_encoded)):
			self.values += [self.values[i-1] + self._delta_encoded[i]]

	def get_short_suffix(self):
		return "model_index ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | model_index  | {:6} shorts".format(self.TAG, len(self.values)))

	def web_repr(self):
		return {"name": "Indexes", "type": "text", "readonly": True, "content": "{} indexes".format(len(self.values))}

###

class Vertex(object):
	def __init__(self, xyz, nxyz, uv):
		self.x, self.y, self.z = xyz
		self.nx, self.ny, self.nz = nxyz
		self.u, self.v = uv

		def float12(x):
			return x/4096.0

		self.x = float12(self.x)
		self.y = float12(self.y)
		self.z = float12(self.z)

		self.nx = float12(self.nx)
		self.ny = float12(self.ny)
		self.nz = float12(self.nz)

		self.u = self.u/16384.0
		self.v = self.v/16384.0

class VertexesSection(dat1lib.types.sections.Section): # aka model_std_vert
	TAG = 0xA98BE69B
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 38298 occurrences in 38298 files (always present)
		# size = 48..17727456 (avg = 49041.9)
		# always last
		#
		# examples: 803D66A8B5147C41 (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 37144 occurrences in 37147 files
		# size = 48..12826640 (avg = 38259.5)
		#
		# examples: 83C4C8562CDC453B (min size), 90B61AD0494B91C9 (max size)

		"""
		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		# self.vertexes = [Vertex(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]
		# self.alternative = list(struct.unpack("<" + "h"*(8*count), data))
		# self.alternative = list(struct.unpack("<h" + "f"*(4*count - 1) + "h", data))

		BUF_SIZE = len(data)//8
		buffers = [struct.unpack("<" + "h" * (BUF_SIZE//2), data[i*BUF_SIZE:(i+1)*BUF_SIZE]) for i in range(8)]
		"""

		self.vertexes = []
		BUFS = 8
		MAX_BUF_SIZE = 0x10000

		for offset in range(0, len(data), BUFS*MAX_BUF_SIZE):
			end = min(offset + BUFS*MAX_BUF_SIZE, len(data))
			batch = data[offset:end]
			buf_size = (end - offset)//BUFS

			buffers = []
			for i in range(BUFS):
				buffers += [[]]

			for i in range(BUFS):
				buffers[i] += list(struct.unpack("<{}h".format(buf_size//2), batch[i*buf_size:(i+1)*buf_size]))

			X, Y, Z = 0, 0, 0
			NX, NY, NZ = 0, 0, 0
			U, V = 0, 0
			for i in range(len(buffers[0])):
				x, y, z = buffers[2][i], buffers[3][i], buffers[4][i]
				nx, ny, nz = buffers[0][i], buffers[1][i], buffers[5][i]
				u, v = buffers[6][i], buffers[7][i]
				X ^= x
				Y ^= y
				Z ^= z
				NX ^= nx
				NY ^= ny
				NZ ^= nz
				U ^= u
				V ^= v
				self.vertexes += [Vertex((X, Y, Z), (NX, NY, NZ), (U, V))]

	def get_short_suffix(self):
		return "vertexes ({})".format(len(self.vertexes))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Vertexes     | {:6} vertexes".format(self.TAG, len(self.vertexes)))
		if config.get("web", False):
			return
		
		print("")
		#######........ | 123  12345678  12345678  12345678  12345678  12345678  12345678
		print("           #           x         y         z        nx        ny        nz         U         V")
		print("         -------------------------------------------------------------------------------------")
		for i, l in enumerate(self.vertexes[:32]):
			print("         - {:<3}  {:8.3}  {:8.3}  {:8.3}  {:8.3}  {:8.3}  {:8.3}  {:8.3}  {:8.3}".format(i, l.x, l.y, l.z, l.nx, l.ny, l.nz, l.u, l.v))
		print("...")
		print("")

	def web_repr(self):
		return {"name": "Vertexes", "type": "text", "readonly": True, "content": "{} vertexes".format(len(self.vertexes))}

###

class x6B855EED_Section(dat1lib.types.sections.Section):
	TAG = 0x6B855EED
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 1017 occurrences in 38298 files
		# size = 16..4431864 (avg = 108495.7)
		#
		# examples: 91F17B2F202041FD (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 1025 occurrences in 37147 files
		# size = 16..3206660 (avg = 123562.4)
		#
		# examples: 9D70551B3BB56B53 (min size), 90B61AD0494B91C9 (max size)

		# same amount as vertexes
		# looks like a bunch of uints
		self.values = utils.read_struct_N_array_data(data, len(data)//4, "<I")

	def get_short_suffix(self):
		return "? ({})".format(len(self.values))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | ?            | {:6} uints".format(self.TAG, len(self.values)))
		print(self.values[:32], "...", self.values[-32:])
		print("")

	def web_repr(self):
		return {"name": "Vertex-related 1", "type": "text", "readonly": True, "content": "{} uints".format(len(self.values))}

class x5CBA9DE9_Section(dat1lib.types.sections.Section):
	TAG = 0x5CBA9DE9
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 11302 occurrences in 38298 files
		# size = 16..4431864 (avg = 18953.2)
		#
		# examples: 9322A1EA95E1B12C (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 11523 occurrences in 37147 files
		# size = 16..3206660 (avg = 14074.3)
		#
		# examples: 9322A1EA95E1B12C (min size), 90B61AD0494B91C9 (max size)
		
		# same amount as vertexes
		# has a lot of 0s
		self.values = utils.read_struct_N_array_data(data, len(data)//4, "<I")

	def get_short_suffix(self):
		return "? ({})".format(len(self.values))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | ?            | {:6} uints".format(self.TAG, len(self.values)))
		print(self.values[:32], "...", self.values[-32:])
		#s = set(self.values)
		#print(len(s), min(s), max(s))
		print("")

	def web_repr(self):
		return {"name": "Vertex-related 2", "type": "text", "readonly": True, "content": "{} uints".format(len(self.values))}

