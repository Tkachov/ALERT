import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class IndexesSection(dat1lib.types.sections.Section):
	TAG = 0x0859863D # Model Index
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

		# RCRA
		# 11363 occurrences in 11387 files
		# size = 6..20930436 (avg = 120896.1)
		#
		# examples: 8FE2973E7E447C52 (min size), 8D14D85B15DFB268 (max size)

		self.version = self._dat1.version
		if self.version is None:
			self.version = dat1lib.VERSION_MSMR

		self.values = []

		if self.version == dat1lib.VERSION_MSMR:
			self._delta_encoded = utils.read_struct_N_array_data(data, len(data)//2, "<h")

			if len(self._delta_encoded) > 0:
				self.values += [self._delta_encoded[0]]

			for i in range(1, len(self._delta_encoded)):
				self.values += [self.values[i-1] + self._delta_encoded[i]]

			for i in range(len(self.values)):
				self.values[i] %= 2**16

		elif self.version == dat1lib.VERSION_RCRA:
			self.values = utils.read_struct_N_array_data(data, len(data)//2, "<h")

	def get_short_suffix(self):
		return "model_index ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | model_index  | {:6} shorts".format(self.TAG, len(self.values)))

	def web_repr(self):
		return {"name": "Indexes", "type": "text", "readonly": True, "content": "{} indexes".format(len(self.values))}

###

class Vertex_I20(object):
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

class Vertex_I29(object):
	def __init__(self, xyz, nxyz, uv):
		self.x, self.y, self.z = xyz
		self.nx, self.ny, self.nz = nxyz
		self.u, self.v = uv

class VertexesSection(dat1lib.types.sections.Section):
	TAG = 0xA98BE69B # Model Std Vert
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

		# RCRA
		# 11363 occurrences in 11387 files
		# size = 48..42789840 (avg = 295514.4)
		#
		# examples: 8FE2973E7E447C52 (min size), AE2DF2353798682F (max size)

		"""
		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		# self.vertexes = [Vertex(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]
		# self.alternative = list(struct.unpack("<" + "h"*(8*count), data))
		# self.alternative = list(struct.unpack("<h" + "f"*(4*count - 1) + "h", data))

		BUF_SIZE = len(data)//8
		buffers = [struct.unpack("<" + "h" * (BUF_SIZE//2), data[i*BUF_SIZE:(i+1)*BUF_SIZE]) for i in range(8)]
		"""

		self.version = self._dat1.version
		if self.version is None:
			self.version = dat1lib.VERSION_MSMR

		self.vertexes = []

		if self.version == dat1lib.VERSION_MSMR:
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
					self.vertexes += [Vertex_I20((X, Y, Z), (NX, NY, NZ), (U, V))]

		elif self.version == dat1lib.VERSION_RCRA:
			scale = 1/4096.0
			for i in range(0, len(data), 16):
				X, Y, Z, NX, NY, NZ, U, V = struct.unpack("<8h", data[i:i+16])
				X *= scale
				Y *= scale
				Z *= scale
				self.vertexes += [Vertex_I29((X, Y, Z), (NX, NY, NZ), (U, V))]

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

		# RCRA
		# 7112 occurrences in 11387 files
		# size = 16..10697472 (avg = 89783.0)
		#
		# examples: 855A86B217E053FB (min size), AE2DF2353798682F (max size)

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

		# RCRA
		# 1807 occurrences in 11387 files
		# size = 16..10697472 (avg = 206608.6)
		#
		# examples: 836851DCBEA9E885 (min size), AE2DF2353798682F (max size)
		
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

#

class xCCBAFF15_Section(dat1lib.types.sections.Section):
	TAG = 0xCCBAFF15
	TYPE = 'ModelRcra'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: none
		# MM: none

		# RCRA
		# 954 occurrences in 11387 files
		# size = 32..21394920 (avg = 789337.3)
		#
		# examples: 8B4C8E19832AE134 (min size), AE2DF2353798682F (max size)

		# typically, the size of this section is ~x2 of 6B855EED and 5CBA9DE9
		# so, same amount as vertexes?
		
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
		return "CCBAFF15 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | CCBAFF15     | {:6} entries".format(self.TAG, len(self.entries)))

