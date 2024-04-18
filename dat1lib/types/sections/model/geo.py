# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct
import math

class IndexesSection(dat1lib.types.sections.Section):
	TAG = 0x0859863D # Model Index
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 8775 occurrences in 8780 files
		# size = 6..2667096 (avg = 24884.3)
		#
		# examples: 2AD6B126 (min size), 7929FC02 (max size)

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

		elif self.version == dat1lib.VERSION_RCRA or self.version == dat1lib.VERSION_SO:
			self.values = utils.read_struct_N_array_data(data, len(data)//2, "<H")

	def save(self):
		if self.version == dat1lib.VERSION_SO:
			return self._raw
			return None # TODO

		if self.version == dat1lib.VERSION_RCRA:
			of = io.BytesIO(bytes())
			for v in self.values:
				of.write(struct.pack("<H", v))
			of.seek(0)
			return of.read()

		def short_overflow(v):
			while v < -0x7FFF - 1:
				v += 2**16

			while v > 0x7FFF:
				v -= 2**16

			return v

		of = io.BytesIO(bytes())
		prev = 0
		for v in self.values:
			of.write(struct.pack("<h", short_overflow(v - prev)))
			prev = v
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "model_index ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | model_index  | {:6} shorts".format(self.TAG, len(self.values)))

	def web_repr(self):
		return {"name": "Indexes", "type": "text", "readonly": True, "content": "{} indexes".format(len(self.values))}

###

def _decode_normal(norm):
	norm = norm & 0xFFFFFFFF
	nx = float((norm & 0x3FF)) * 0.00276483595 - math.sqrt(2)
	ny = float(((norm >> 10) & 0x3FF)) * 0.00276483595 - math.sqrt(2)
	flip = (norm >> 31) == 0

	nxxyy = nx * nx + ny * ny
	nw = 0
	try:
		nw = math.sqrt(1 - 0.25 * nxxyy)
	except:
		pass

	nx = nx * nw
	ny = ny * nw
	nz = 1 - 0.5 * nxxyy

	if flip:
		nz = -nz

	return (nx, ny, nz)

class Vertex_I20(object):
	def __init__(self, xyz, nxyz, uv):
		self.x, self.y, self.z = xyz
		self.nx, self.ny, self.nz = _decode_normal(nxyz)
		self.u, self.v = uv

		def float12(x):
			return x/4096.0

		self.x = float12(self.x)
		self.y = float12(self.y)
		self.z = float12(self.z)

		self.u = self.u
		self.v = self.v

		self.tangent = None
		self.bitangent = None

class Vertex_I29(object):
	def __init__(self, xyz, nxyz, uv):
		self.x, self.y, self.z = xyz
		self.nx, self.ny, self.nz = 1, 0, 0
		self.u, self.v = uv

		#

		scale = 1/4096.0

		self.x *= scale
		self.y *= scale
		self.z *= scale

		#

		self.nx, self.ny, self.nz = _decode_normal(nxyz)

		#

		self.u = self.u/32768.0
		self.v = self.v/32768.0

	@classmethod
	def empty(cls):
		return cls((0,0,0), 0, (0,0))

	def save(self):
		scale = 1/4096.0
		X, Y, Z, W = self.x / scale, self.y / scale, self.z / scale, 0
		X, Y, Z = int(X), int(Y), int(Z)

		nX = (self.nx + 1.0)*511.0
		nY = (self.ny + 1.0)*511.0
		nZ = (self.nz + 1.0)*2047.0
		nX = int(nX)
		nY = int(nY)
		nZ = int(nZ)
		nX = struct.unpack("<H", struct.pack("<h", nX))[0]
		nY = struct.unpack("<H", struct.pack("<h", nY))[0]
		nZ = struct.unpack("<H", struct.pack("<h", nZ))[0]	
		NXYZ = (nX & 0b1111111111) | ((nY & 0b1111111111) << 10) | ((nZ & 0b111111111111) << 20) # TODO: this is wrong normals encoding

		U = self.u * 32768.0
		V = self.v * 32768.0
		U, V = int(U), int(V)

		return struct.pack("<4hI2h", X, Y, Z, W, NXYZ, U, V)

class VertexesSection(dat1lib.types.sections.Section):
	TAG = 0xA98BE69B # Model Std Vert
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 8775 occurrences in 8780 files
		# size = 48..8854176 (avg = 56787.4)
		#
		# examples: 2AD6B126 (min size), 7929FC02 (max size)

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

				N_buffer = list(struct.unpack("<{}I".format(buf_size//2), batch[0:2*buf_size]))

				N = 0
				X, Y, Z = 0, 0, 0
				U, V = 0, 0

				for i in range(len(buffers[0])):
					x, y, z, _ = buffers[2][i], buffers[3][i], buffers[4][i], buffers[5][i]
					u, v = buffers[6][i], buffers[7][i]
					N ^= N_buffer[i]
					X ^= x
					Y ^= y
					Z ^= z
					U ^= u
					V ^= v
					self.vertexes += [Vertex_I20((X, Y, Z), N, (U, V))]

		elif self.version == dat1lib.VERSION_RCRA or self.version == dat1lib.VERSION_SO:
			for i in range(0, len(data), 16):
				X, Y, Z, W, NXYZ, U, V = struct.unpack("<4hI2h", data[i:i+16])
				self.vertexes += [Vertex_I29((X, Y, Z), NXYZ, (U, V))]

	def save(self):
		of = io.BytesIO(bytes())
		
		if self.version == dat1lib.VERSION_RCRA:
			for e in self.vertexes:
				of.write(e.save())
		else:
			MAX_BATCH = 0x8000

			mscale = 1.0/4096.0
			uv_scale = 1.0/16384.0
		
			SECTION_BUILT = 0x283D0383
			s = self._dat1.get_section(SECTION_BUILT)
			if s:
				uv_scale = s.get_uv_scale()

			def clamp_short(v):
				return min(max(-0x7FFF - 1, v), 0x7FFF)

			def clamp_ushort(v):
				return min(max(0, v), 0xFFFF)

			def encode_position(pos, scale):
				return clamp_short(int(round(pos / scale)))

			def encode_texcoord(pos, scale):
				pos = int(round(pos / scale))
				return clamp_short(pos)

			def _encode_normal(nx, ny, nz):
				flip = 1
				if nz < 0:
					nz = -nz
					flip = 0

				nxxyy = (1 - nz)*2.0
				nw = 0
				try:
					nw = math.sqrt(1 - 0.25*nxxyy)
				except:
					pass
				if nw > 0:
					nx = nx/nw
					ny = ny/nw
				
				c = math.sqrt(2) / (0x3FF / 2.0)
				n1 = int(round((nx + math.sqrt(2)) / c)) & 0x3FF
				n2 = int(round((ny + math.sqrt(2)) / c)) & 0x3FF
				
				return (flip<<31) | (n2<<10) | n1

			def encode_tangents(n, t, b):
				def vec_mult_scalar(vc, sc):
					return (vc[0] * sc, vc[1] * sc, vc[2] * sc)

				def vec_minus_vec(vc1, vc2):
					return (vc1[0] - vc2[0], vc1[1] - vc2[1], vc1[2] - vc2[2])

				def vec_plus_vec(vc1, vc2):
					return (vc1[0] + vc2[0], vc1[1] + vc2[1], vc1[2] + vc2[2])

				def vec_dot(vc1, vc2):
					return (vc1[0] * vc2[0]) + (vc1[1] * vc2[1]) + (vc1[2] * vc2[2])

				def vec_length(vc):
					return math.sqrt(vec_dot(vc, vc))

				def vec_normalize(vc):
					l = vec_length(vc)
					if l <= 0:
						return (1, 0, 0)
					return (vc[0]/l, vc[1]/l, vc[2]/l)

				def vec_cross(a, b):
					a1, a2, a3 = a
					b1, b2, b3 = b
					return (a2*b3 - a3*b2, a3*b1 - a1*b3, a1*b2 - a2*b1)

				sqr2 = math.sqrt(2) * 2

				thisn = n
				thist = vec_minus_vec(t, vec_mult_scalar(thisn, vec_dot(thisn, t)))
				thist = vec_normalize(thist)
				btsign = 0
				if vec_length(t) > 0 and vec_length(b) > 0:
					t = vec_normalize(t)
					b = vec_normalize(b)
					cr = vec_cross(t, b)
					bts = vec_dot(cr, thisn)
					if bts > 0:
						btsign = 1
					else:
						btsign = -1

				n3 = n[2]
				nsign = 1
				if n3 < 0:
					nsign = -1
					n3 = -n3

				sqrxy = math.sqrt(1 - (1 - n3) / 2.0)
				n1 = n[0] / sqrxy
				n2 = n[1] / sqrxy
				n1 = n1 / sqr2 + 0.5
				n2 = n2 / sqr2 + 0.5

				n1 = min(max(0, n1), 1)
				n2 = min(max(0, n2), 1)

				norm1 = int(n2 * 1023) << 10
				norm1 |= int(n1 * 1023)
				
				n3 = thist[2]
				tsign = 1
				if n3 < 0:
					tsign = -1
					n3 = -n3

				sqrxy = math.sqrt(1 - (1 - n3) / 2.0)
				n1 = thist[0] / sqrxy
				n2 = thist[1] / sqrxy
				n1 = n1 / sqr2 + 0.5
				n2 = n2 / sqr2 + 0.5

				n1 = min(max(0, n1), 1)
				n2 = min(max(0, n2), 1)

				norm1 |= int(n1 * 1023) << 20
				if nsign > 0:
					norm1 |= 0x80000000
				if tsign > 0:
					norm1 |= 0x40000000
				rv1 = norm1 & (0x7FF<<20)
				rv1 |= _encode_normal(*n)

				norm1 = int(n2 * 1023)
				norm1 |= 0x7C00
				if btsign > 0:
					norm1 = ~norm1 + 1
				rv2 = clamp_short(norm1)

				return (rv1, rv2)

			ln = len(self.vertexes)
			for i in range(0, ln, MAX_BATCH):
				batch_end = i + MAX_BATCH
				if batch_end > ln:
					batch_end = ln
				batch = self.vertexes[i:batch_end]

				# normal/tangent
				prev = 0
				for v in batch:
					curr = 0x7FF80200
					if v.tangent is not None and v.bitangent is not None:
						curr, _ = encode_tangents((v.nx, v.ny, v.nz), v.tangent, v.bitangent)
					of.write(struct.pack("<I", prev ^ curr))
					prev = curr
				
				# x
				prev = 0
				for v in batch:
					curr = encode_position(v.x, mscale)
					of.write(struct.pack("<h", prev ^ curr))
					prev = curr

				# y
				prev = 0
				for v in batch:
					curr = encode_position(v.y, mscale)
					of.write(struct.pack("<h", prev ^ curr))
					prev = curr

				# z
				prev = 0
				for v in batch:
					curr = encode_position(v.z, mscale)
					of.write(struct.pack("<h", prev ^ curr))
					prev = curr

				# bitangent
				prev = 0
				for v in batch:
					curr = 0x7E
					if v.tangent is not None and v.bitangent is not None:
						_, curr = encode_tangents((v.nx, v.ny, v.nz), v.tangent, v.bitangent)
					of.write(struct.pack("<h", prev ^ curr))
					prev = curr

				# u
				prev = 0
				for v in batch:
					curr = encode_texcoord(v.u, uv_scale)
					of.write(struct.pack("<h", prev ^ curr))
					prev = curr

				# v
				prev = 0
				for v in batch:
					curr = encode_texcoord(v.v, uv_scale)
					of.write(struct.pack("<h", prev ^ curr))
					prev = curr

		of.seek(0)
		return of.read()

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
	TAG = 0x6B855EED # Model UV1 Vert
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
		self.uvs = utils.read_struct_array_data(data, "<2h")

	def save(self):
		of = io.BytesIO(bytes())
		for uv in self.uvs:
			of.write(struct.pack("<2h", *uv))
		of.seek(0)
		return of.read()

	def get_uv(self, index):
		u, v = self.uvs[index]
		u = u / 32768.0
		v = v / 32768.0
		return (u, v)

	def set_uv(self, index, u, v):
		u = u * 32768.0
		v = v * 32768.0
		self.uvs[index] = (int(u), int(v))

	def get_short_suffix(self):
		return "UV1s ({})".format(len(self.uvs))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Vertex UV1   | {:6} UVs".format(self.TAG, len(self.uvs)))
		print("")

	def web_repr(self):
		return {"name": "Vertex UV1", "type": "text", "readonly": True, "content": "{} UVs".format(len(self.values))}

class ColorsSection(dat1lib.types.sections.Section):
	TAG = 0x5CBA9DE9 # Model Col Vert
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 1425 occurrences in 8780 files
		# size = 16..2213544 (avg = 22159.5)
		#
		# examples: 08BEC68D (min size), 7929FC02 (max size)

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
		
		self.values = utils.read_struct_N_array_data(data, len(data)//4, "<I") # "<4B"

	def save(self):
		of = io.BytesIO(bytes())
		for v in self.values:
			of.write(struct.pack("<I", v))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "colors ({})".format(len(self.values))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Vertex Color | {:6} colors".format(self.TAG, len(self.values)))
		print("")

	def web_repr(self):
		return {"name": "Vertex Colors", "type": "text", "readonly": True, "content": "{} colors".format(len(self.values))}
