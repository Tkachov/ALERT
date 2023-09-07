import dat1lib
import dat1lib.types.model
import dat1lib.types.sections.model.geo
import dat1lib.types.sections.model.look
import dat1lib.types.sections.model.meshes
import dat1lib.types.sections.model.skin
import dat1lib.types.sections.model.unknowns
import struct

SECTION_INDEXES     = dat1lib.types.sections.model.geo.IndexesSection.TAG
SECTION_VERTEXES    = dat1lib.types.sections.model.geo.VertexesSection.TAG
SECTION_LOOK        = dat1lib.types.sections.model.look.ModelLookSection.TAG
SECTION_MESHES      = dat1lib.types.sections.model.meshes.MeshesSection.TAG
SECTION_SKIN_BATCH  = dat1lib.types.sections.model.skin.ModelSkinBatchSection.TAG
SECTION_SKIN_DATA   = dat1lib.types.sections.model.skin.ModelSkinDataSection.TAG
SECTION_RCRA_SKIN   = dat1lib.types.sections.model.skin.xCCBAFF15_Section.TAG
SECTION_MATERIALS   = dat1lib.types.sections.model.unknowns.ModelMaterialSection.TAG

def _pretty_format(n):
	s = f"{n:.6f}"
	i = s.index(".")
	if i != -1:
		j = len(s)
		while j > i:
			if s[j-1] == '0':
				j -= 1
			else:
				break
		if j == i+1:
			return s[:i]
		return s[:j]
	return s

def pretty_format(n):
	s = _pretty_format(n)
	if s == "-0":
		return "0"
	return s

###

# math

def QxQ(q, p):
	aq, bq, cq, dq = q
	ap, bp, cp, dp = p

	return (
		dq * ap + aq * dp + bq * cp - cq * bp,
		dq * bp - aq * cp + bq * dp + cq * ap,
		dq * cp + aq * bp - bq * ap + cq * dp,
		dq * dp - aq * ap - bq * bp - cq * cp
	)

def QxV(q, v):
	ax, ay, az, aw = q
	bx, by, bz = v
	return (
		aw * bx + ay * bz - az * by,
		aw * by - ax * bz + az * bx,
		aw * bz + ax * by - ay * bx,
		-ax * bx - ay * by - az * bz
	)

def invQ(q):
	x,y,z,w = q
	return (-x, -y, -z, w)

def rotV(v, q):
	t = QxV(q, v)
	t = QxQ(t, invQ(q))
	return t[:3]

def v_plus(a, b):
	return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

###

class AsciiWriter(object):
	def __init__(self):
		self.init(None, None)

	def init(self, f, model):
		self.f = f
		self.model = model
		self.current_vertex_index = 0

		self.vertexes = []
		if model is not None:
			s = model.dat1.get_section(SECTION_VERTEXES)
			self.vertexes = s.vertexes

		self.meshes = []
		if model is not None:
			s = model.dat1.get_section(SECTION_MESHES)
			self.meshes = s.meshes

		self.materials_section = None if model is None else model.dat1.get_section(SECTION_MATERIALS)

	#

	def write_model(self, f, model, looks, lod):
		self.init(f, model)

		meshes_indexes = self.get_meshes_indexes_by_looks_and_lod(looks, lod)
		skin, rcra_skin = self.get_skin()

		self.write_bones()
		self.write_meshes(meshes_indexes, skin, rcra_skin)

	#

	def get_skin(self):
		skin_section = self.model.dat1.get_section(SECTION_SKIN_DATA)
		skin_batch_section = self.model.dat1.get_section(SECTION_SKIN_BATCH)

		has_skin = (skin_section is not None and skin_batch_section is not None)
		skin = None
		rcra_skin = None

		if has_skin:
			skin = []

			has_to_be_len = 0
			for i, l in enumerate(skin_batch_section.batches):
				offset = l.offset
				count = l.vertex_count

				for j in range(0, count, 16):
					groups = skin_section._raw[offset] + 1
					offset += 1

					for z in range(16):
						if j + z >= count:
							break

						vertex = []

						if groups == 1:
							bone = skin_section._raw[offset]
							offset += 1
							vertex += [(bone, 1.0)]
						else:
							for k in range(groups):
								bone, weight = struct.unpack("<BB", skin_section._raw[offset:offset+2])
								offset += 2
								vertex += [(bone, weight/256.0)]

						skin += [vertex]

			def fix_weights(v):
				mp = {}
				order = []
				for b, w in v:
					mp[b] = mp.get(b, 0) + w
					if b not in order:
						order += [b]
				return [(b, mp[b]) for b in order]

			skin = [fix_weights(v) for v in skin]

		#

		rcra_skin_section = self.model.dat1.get_section(SECTION_RCRA_SKIN)
		if rcra_skin_section is not None:
			rcra_skin = []
			for v in rcra_skin_section.entries:
				b1, b2, b3, b4, w1, w2, w3, w4 = v
				
				temp = {}
				temp[b1] = w1
				temp[b2] = temp.get(b2, 0) + w2
				temp[b3] = temp.get(b3, 0) + w3
				temp[b4] = temp.get(b4, 0) + w4

				sm = w1 + w2 + w3 + w4
				if sm > 0 and sm != 1:
					for k in temp:
						temp[k] = temp[k] / sm

				weights = [(k, temp[k]) for k in temp]
				weights = sorted(weights, key=lambda x: -x[1])
				weights = [w for w in weights if w[1] > 0]

				rcra_skin += [weights]

			if has_skin:
				def diff_skins(skin, rcra_skin):
					def same_weights(v1, v2):
						if len(v1) != len(v2):
							return False

						for a, b in zip(v1, v2):
							b1, w1 = a
							b2, w2 = b
							if b1 != b2 or abs(w1 - w2) >= 0.01:
								return False

						return True

					print(len(skin), len(rcra_skin))
					same = True
					for v1, v2 in zip(skin, rcra_skin):
						if not same_weights(v1, v2):
							print(v1, v2)
							same = False
							# break
					if same:
						print("same skin")

				# diff_skins(skin, rcra_skin)

			# skin = rcra_skin
			# has_skin = True

		#

		return skin, rcra_skin

	def get_weights(self, i, skin, weights_count):
		vertex = skin[i]
		fmt = pretty_format

		groups = ""
		weights = ""
		for j in range(weights_count):
			if groups != "":
				groups += " "
				weights += " "

			g = 0
			w = 0
			if j < len(vertex):
				g, w = vertex[j]
				if w == 0:
					g = 0

			groups += f"{g}"
			weights += f"{fmt(w)}"

		return groups, weights

	#

	def get_meshes_indexes_by_looks_and_lod(self, looks, lod):
		looks_section = self.model.dat1.get_section(SECTION_LOOK)

		meshes_to_display = set()
		for look in looks:
			look_lod = looks_section.looks[look].lods[lod]
			meshes_to_display |= set(range(look_lod.start, look_lod.start + look_lod.count))

		meshes_indexes = []
		for i, mesh in enumerate(self.meshes):
			if i not in meshes_to_display:
				continue

			meshes_indexes += [i]

		return meshes_indexes

	#

	def write_bones(self):
		joints_section = self.model.dat1.get_section(0x15DF9D3B)
		joints_transform_section = self.model.dat1.get_section(0xDCC88A19)
		memoized = {}

		def get_transform(i, memoized, joints_section, joints_transform_section):
			mm = memoized.get(i, None)
			if mm is not None:
				return mm

			x, y, z = joints_transform_section.get_joint_position(i)
			qx, qy, qz, qw = joints_transform_section.get_joint_quaternion(i)

			j = joints_section.joints[i]
			if j.parent != -1:
				t = get_transform(j.parent, memoized, joints_section, joints_transform_section)

				parent_pos = t[:3]
				parent_q = t[3:]

				qx, qy, qz, qw = QxQ(parent_q, (qx, qy, qz, qw))
				x, y, z = v_plus(parent_pos, rotV((x, y, z), parent_q))

			mm = (x, y, z, qx, qy, qz, qw)
			memoized[i] = mm
			return mm

		fmt = pretty_format

		self.f.write(f"{len(joints_section.joints)}\n")
		for i, j in enumerate(joints_section.joints):
			name = self.model.dat1.get_string(j.string_offset)
			x, y, z, qx, qy, qz, qw = get_transform(i, memoized, joints_section, joints_transform_section)

			self.f.write(f"{name}\n")
			self.f.write(f"{j.parent}\n")
			self.f.write(f"{fmt(x)} {fmt(y)} {fmt(z)} {fmt(qx)} {fmt(qy)} {fmt(qz)} {fmt(qw)}\n")

	def write_meshes(self, meshes_indexes, skin, rcra_skin):
		self.f.write("{}\n".format(len(meshes_indexes)))
		for mi in meshes_indexes:
			self.write_mesh(mi, skin, rcra_skin)

	def write_mesh(self, mesh_index, skin, rcra_skin):
		vc = self.current_vertex_index

		mesh = self.meshes[mesh_index]
		matpath = self.model.dat1.get_string(self.materials_section.string_offsets[mesh.get_material()][0])
		self.f.write(f"sm{mesh_index:02}_{matpath}\n")

		groups_count = 4
		for vi in range(mesh.vertexStart, mesh.vertexStart + mesh.vertexCount):
			groups_count = max(len(skin[vi]), groups_count)

		uv_layers = 1
		self.f.write("{}\n".format(uv_layers))
		self.f.write("0\n") # textures

		# vertexes

		skin_to_use = skin
		weight_offset = mesh.vertexStart
		if (mesh.get_flags() & 0x100) > 0:
			skin_to_use = rcra_skin
			weight_offset = mesh.first_weight_index
		
		self.f.write("{}\n".format(mesh.vertexCount))
		for vi in range(mesh.vertexStart, mesh.vertexStart + mesh.vertexCount):
			self.write_vertex(vi, skin_to_use, vi - mesh.vertexStart + weight_offset, groups_count)

		# indexes

		s = self.model.dat1.get_section(SECTION_INDEXES)
		indexes = s.values
		
		if (mesh.get_flags() & 0x10) > 0:
			vc = 0 # indexes are relative already

		faces_count = mesh.indexCount // 3
		self.f.write("{}\n".format(faces_count))
		for j in range(faces_count):
			index_index = mesh.indexStart + j*3
			self.f.write("{} {} {}\n".format(indexes[index_index+2]-vc, indexes[index_index+1]-vc, indexes[index_index]-vc))

	def write_vertex(self, vertex_index, skin, weight_index, groups_count):
		fmt = pretty_format
		v = self.vertexes[vertex_index]
		
		position = f"{fmt(v.x)} {fmt(v.y)} {fmt(v.z)}"
		normal = f"{fmt(v.nx)} {fmt(v.ny)} {fmt(v.nz)}"
		color = "0 0 0 0"
		uv = f"{fmt(v.u)} {fmt(v.v)}"
		groups = "0 0 0 0"
		weights = "1 0 0 0"

		if skin is not None:
			groups, weights = self.get_weights(weight_index, skin, groups_count)

		self.f.write(position + "\n")
		self.f.write(normal + "\n")
		self.f.write(color + "\n")
		self.f.write(uv + "\n")
		self.f.write(groups + "\n")
		self.f.write(weights + "\n")

		self.current_vertex_index += 1

###

import sys

import dat1lib
import dat1lib.types.dat1
import dat1lib.types.model

###

def main(argv):
	if len(argv) < 2:
		print("Usage:")
		print("$ {} <.model filename> [output .ascii filename]".format(argv[0]))
		return

	#

	fn = argv[1]
	model = None
	try:
		with open(fn, "rb") as f:
			model = dat1lib.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(fn))
		print(e)
		return

	#
	
	if model is None:
		print("[!] Couldn't comprehend '{}'".format(fn))
		return

	if not isinstance(model, dat1lib.types.model.ModelRcra):
		print("[!] Not a model")
		return

	#

	output_fn = fn + ".ascii"
	if len(argv) > 2:
		output_fn = argv[2]

	with open(output_fn, "w") as f:
		looks = [0]
		lod = 0
		helper = AsciiWriter()
		helper.write_model(f, model, looks, lod)

if __name__ == "__main__":
	main(sys.argv)
