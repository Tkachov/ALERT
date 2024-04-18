# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib
import dat1lib.types.model
import dat1lib.types.sections.model.geo
import dat1lib.types.sections.model.look
import dat1lib.types.sections.model.meshes
import dat1lib.types.sections.model.skin
import dat1lib.types.sections.model.unknowns
import dat1lib.utils as utils
import struct

SECTION_INDEXES     = dat1lib.types.sections.model.geo.IndexesSection.TAG
SECTION_VERTEXES    = dat1lib.types.sections.model.geo.VertexesSection.TAG
SECTION_UV1         = dat1lib.types.sections.model.geo.x6B855EED_Section.TAG
SECTION_LOOK        = dat1lib.types.sections.model.look.ModelLookSection.TAG
SECTION_MESHES      = dat1lib.types.sections.model.meshes.MeshesSection.TAG
SECTION_SKIN_BATCH  = dat1lib.types.sections.model.skin.ModelSkinBatchSection.TAG
SECTION_SKIN_DATA   = dat1lib.types.sections.model.skin.ModelSkinDataSection.TAG
SECTION_RCRA_SKIN   = dat1lib.types.sections.model.skin.xCCBAFF15_Section.TAG
SECTION_BUILT       = dat1lib.types.sections.model.unknowns.ModelBuiltSection.TAG
SECTION_MATERIALS   = dat1lib.types.sections.model.unknowns.ModelMaterialSection.TAG

###

class AsciiReader(object):
	def __init__(self):
		self.f = None
		self.lines = []
		self.ptr = 0

	#

	def read(self, f):
		self.lines = f.read().split("\n")
		self.clean_lines()
		self.ptr = 0

		result = {}		
		result["bones"] = self.read_bones()
		result["meshes"] = self.read_meshes()

		return result

	def read_bones(self):
		bones = []

		bones_count = self.read_int()
		for i in range(bones_count):
			name = self.read_line()
			parent = self.read_int()
			parts = self.read_split()
			bones += [(name, parent, (float(parts[0]), float(parts[1]), float(parts[2])))]

		return bones

	def read_meshes(self):
		meshes = []

		meshes_count = self.read_int()
		for i in range(meshes_count):
			name = self.read_line()
			uv_layers = self.read_int()
			textures = self.read_int()			
			self.skip(textures*2)

			vertexes = self.read_vertexes(uv_layers)
			faces = self.read_faces()

			meshes += [(name, uv_layers, textures, vertexes, faces)]

		return meshes

	def read_vertexes(self, uv_layers):
		vertexes = []

		vertexes_count = self.read_int()
		for j in range(vertexes_count):
			position = self.read_split()
			normal = self.read_split()
			color = self.read_split()

			uv = None
			if uv_layers > 0:
				uv = self.read_split()
				uv = (float(uv[0]), float(uv[1]))
			if uv_layers > 1:
				self.skip(uv_layers - 1)

			groups = self.read_split()
			weights = self.read_split()

			vertexes += [
				(
					(float(position[0]), float(position[1]), float(position[2])),
					(float(normal[0]), float(normal[1]), float(normal[2])),
					color,
					uv,
					[int(x) for x in groups],
					[float(x) for x in weights]
				)
			]

		return vertexes

	def read_faces(self):
		faces = []

		faces_count = self.read_int()
		for j in range(faces_count):
			faces += [self.read_line()]

		return faces

	#

	def clean_lines(self):
		result = []

		for l in self.lines:
			if l is None:
				continue

			i = l.find("#")
			if i != -1:
				l = l[:i]

			l = l.strip()
			if l == "":
				continue

			result += [l]
		
		self.lines = result

	#

	def read_line(self):
		result = self.lines[self.ptr]
		self.ptr += 1
		return result

	def peek_line(self):
		return self.lines[self.ptr]

	def skip(self, n=1):
		self.ptr += n

	#

	def read_int(self):
		return int(self.read_line())

	def read_split(self):
		return self.read_line().split(" ")

###

class ModelInjector(object):
	def __init__(self):
		self.init(None)

	def init(self, model):
		self.sections_to_refresh = set()
		self.model = model

		self.mode = dat1lib.VERSION_RCRA
		if not isinstance(self.model, dat1lib.types.model.ModelRcra):
			self.mode = dat1lib.VERSION_MSMR

		self.vertexes_section = None if model is None else model.dat1.get_section(SECTION_VERTEXES)
		self.indexes_section = None if model is None else model.dat1.get_section(SECTION_INDEXES)
		self.current_vertex_index = 0
		self.current_index_index = 0

		self.skin_section = None if model is None else model.dat1.get_section(SECTION_SKIN_DATA)
		self.skin_batch_section = None if model is None else model.dat1.get_section(SECTION_SKIN_BATCH)
		self.batch_vertex_index = 0
		self.sum_batch_vertex_index = 0
		self.batch_vertex_count = 0
		self.weights_group = []
		self.current_skin_batch = 0
		self.current_skin_offset = 0

		self.rcra_weights_section = None if model is None else model.dat1.get_section(SECTION_RCRA_SKIN)
		self.current_rcra_weight_index = 0

		self.uv1_section = None if model is None else model.dat1.get_section(SECTION_UV1)

	#

	def inject(self, model, ascii_data, materials_txt=None):
		self.init(model)

		self.clear_muscle_deformation()
		self.change_lod_distances()

		lg_mats_overrides = {}
		if materials_txt:
			lg_mats_overrides = self.read_materials_txt(materials_txt)

		self.update_lookgroups(ascii_data, lg_mats_overrides)

		meshes_updates = self.inject_vertexes(ascii_data)
		self.update_meshes(meshes_updates, lg_mats_overrides)
		self.calculate_tangents(len(meshes_updates))

		self.refresh_sections()

	def clear_muscle_deformation(self):
		# similarly to how daemon's mi.exe does

		SECTION_MUSCLEDEF = 0x380A5744
		mds = self.model.dat1.get_section(SECTION_MUSCLEDEF)
		if not mds:
			return

		mds._raw[:24] = struct.pack("<6i", 0, 0, 0, 0x40, 0x48, 0)
		mds._raw[0x40:0x40 + 16] = struct.pack("<2q", -1, -1)
		self.refresh_section(SECTION_MUSCLEDEF)

	def change_lod_distances(self):
		# similarly to how daemon's mi.exe does

		bs = self.model.dat1.get_section(SECTION_BUILT)
		if not bs:
			return

		for i in range(5):
			bs.values[0x34//4 + i] = 4096.0
		
		self.refresh_section(SECTION_BUILT)

	def read_materials_txt(self, materials_txt):
		result = {}

		f = open(materials_txt, "r")
		lines = f.read().split("\n")
		f.close()

		ptr = 0
		l = lines[ptr]
		ptr += 1

		if "LookGroups" in l:
			looks_section = self.model.dat1.get_section(SECTION_LOOK)

			lg = []
			for i in range(len(looks_section.looks)):
				parts = lines[ptr].split()
				ptr += 1

				a, b = int(parts[0]), int(parts[1])
				lg += [(a, b)]

			result["lookgroups"] = lg
			ptr += 1

		l = lines[ptr] # "Materials used:"
		ptr += 1

		materials = []
		while True:
			l = lines[ptr]
			ptr += 1
			if l == "":
				break

			parts = l.split()
			materials += [int(parts[0])]

		result["materials"] = materials
		return result

	def update_lookgroups(self, ascii_data, lookgroups_overrides):
		looks_section = self.model.dat1.get_section(SECTION_LOOK)
		looks_count = len(looks_section.looks)

		meshes_count = len(ascii_data["meshes"])
		overrides = [(0, meshes_count)]
		if looks_count > 1:
			overrides += [(0, meshes_count)]

		if "lookgroups" in lookgroups_overrides:
			overrides = lookgroups_overrides["lookgroups"]

		for i in range(len(overrides)):
			look = looks_section.looks[i]
			for j in range(6):
				look.lods[j].start = overrides[i][0]
				look.lods[j].count = overrides[i][1]

		self.refresh_section(SECTION_LOOK)

	def update_meshes(self, meshes_updates, materials_overrides):
		s = self.model.dat1.get_section(SECTION_MATERIALS)
		materials_count = len(s.string_offsets)

		overrides = []
		if "materials" in materials_overrides:
			overrides = materials_overrides["materials"]

		s = self.model.dat1.get_section(SECTION_MESHES)
		meshes = s.meshes

		for i, new_mesh in enumerate(meshes_updates):
			mesh = meshes[i]
			mesh.vertexStart = new_mesh[0]
			mesh.vertexCount = new_mesh[1]
			mesh.indexStart = new_mesh[2]
			mesh.indexCount = new_mesh[3]
			
			if (mesh.get_flags() & 0x10) > 0:
				mesh.first_skin_batch = new_mesh[4]
				mesh.skin_batches_count = new_mesh[6]

			if (mesh.get_flags() & 0x100) > 0:
				mesh.first_weight_index = new_mesh[5]

			mesh.flags = mesh.get_flags() & 0x111

			if i < len(overrides):
				mesh.material_index = overrides[i]
			elif i < materials_count:
				mesh.material_index = i
			else:
				mesh.material_index = 0

		for i in range(len(meshes_updates), len(meshes)):
			meshes[i].clear()

		self.refresh_section(SECTION_MESHES)

	def inject_vertexes(self, ascii_data):
		s = self.model.dat1.get_section(SECTION_MESHES)
		meshes = s.meshes

		meshes_updates = []
		for i, mesh_data in enumerate(ascii_data["meshes"]):
			mesh = meshes[i]
			has_skin = ((mesh.get_flags() & 0x1) > 0)
			has_rcra_skin = ((mesh.get_flags() & 0x100) > 0)

			# name, uv_layers, textures, vertexes, faces
			_, _, _, vertexes_data, faces_data = mesh_data

			vertex_start = self.current_vertex_index
			vertex_count = len(vertexes_data)
			index_start = self.current_index_index
			index_count = len(faces_data) * 3

			first_skin_batch, first_weight_index = self.start_skin_batches(vertex_start, vertex_count)

			prefix = f"mesh #{i}: "
			if len(prefix) < 13:
				prefix += ' ' * (13 - len(prefix))
			print(f"{prefix}writing {vertex_count} vertexes, {index_count} indexes")

			for vertex_data in vertexes_data:
				xyz, nxyz, _, uv, groups_data, weights_data = vertex_data
				self.write_vertex(xyz, nxyz, uv)
				if has_skin:
					w = self.get_vertex_weights(groups_data, weights_data)
					self.write_weight(w)
					if has_rcra_skin:
						self.write_rcra_weight(w)
						

			face_index_offset = vertex_start
			if (mesh.get_flags() & 0x10) > 0:
				face_index_offset = 0 # put relative indexes

			for face in faces_data:
				self.write_face(face, face_index_offset)
			
			skin_batches_count = self.end_skin_batches(first_skin_batch)
			print(f"             added {skin_batches_count} skin batches, {self.current_skin_offset - self.skin_batch_section.batches[first_skin_batch].offset} bytes ({self.current_skin_offset}/{len(self.skin_section._raw)})")
			print()

			meshes_updates += [(vertex_start, vertex_count, index_start, index_count, first_skin_batch, first_weight_index, skin_batches_count)]

		self.refresh_section(SECTION_VERTEXES)
		self.refresh_section(SECTION_INDEXES)
		self.refresh_section(SECTION_SKIN_DATA)
		self.refresh_section(SECTION_SKIN_BATCH)
		self.refresh_section(SECTION_RCRA_SKIN)
		self.refresh_section(SECTION_UV1)

		return meshes_updates

	def calculate_tangents(self, meshes_count):
		tangent = []
		bitangent = []

		for i in range(self.current_vertex_index):
			tangent += [(0, 0, 0)]
			bitangent += [(0, 0, 0)]

		s = self.model.dat1.get_section(SECTION_MESHES)
		meshes = s.meshes
		for mi in range(meshes_count):
			mesh = meshes[mi]

			vs = mesh.vertexStart
			f0 = mesh.indexStart
			nf = mesh.indexCount
			v_offset = vs

			if (mesh.get_flags() & 0x10) > 0:
				v_offset = 0

			for f in range(0, nf, 3):
				i0 = self.indexes_section.values[f0 + f + 2] - v_offset
				i1 = self.indexes_section.values[f0 + f + 1] - v_offset
				i2 = self.indexes_section.values[f0 + f + 0] - v_offset

				v0 = self.vertexes_section.vertexes[vs + i0]
				p0 = (v0.x, v0.y, v0.z)

				v1 = self.vertexes_section.vertexes[vs + i1]
				p1 = (v1.x, v1.y, v1.z)

				v2 = self.vertexes_section.vertexes[vs + i2]
				p2 = (v2.x, v2.y, v2.z)

				def vec_mult_scalar(vc, sc):
					return (vc[0] * sc, vc[1] * sc, vc[2] * sc)

				def vec_minus_vec(vc1, vc2):
					return (vc1[0] - vc2[0], vc1[1] - vc2[1], vc1[2] - vc2[2])

				def vec_plus_vec(vc1, vc2):
					return (vc1[0] + vc2[0], vc1[1] + vc2[1], vc1[2] + vc2[2])

				e1 = vec_minus_vec(p1, p0)
				e2 = vec_minus_vec(p2, p0)

				x1 = v1.u - v0.u
				x2 = v2.u - v0.u
				y1 = v1.v - v0.v
				y2 = v2.v - v0.v
				r = x1*y2 - x2*y1
				if r > 0:
					r = 1.0 / r

				t = vec_mult_scalar(vec_minus_vec(vec_mult_scalar(e1, y2), vec_mult_scalar(e2, y1)), r) # (e1 * y2 - e2 * y1) * r
				b = vec_mult_scalar(vec_minus_vec(vec_mult_scalar(e2, x1), vec_mult_scalar(e1, x2)), r) # (e2 * x1 - e1 * x2) * r

				tangent[vs + i0] = vec_plus_vec(tangent[vs + i0], t)
				tangent[vs + i1] = vec_plus_vec(tangent[vs + i1], t)
				tangent[vs + i2] = vec_plus_vec(tangent[vs + i2], t)

				bitangent[vs + i0] = vec_plus_vec(bitangent[vs + i0], b)
				bitangent[vs + i1] = vec_plus_vec(bitangent[vs + i1], b)
				bitangent[vs + i2] = vec_plus_vec(bitangent[vs + i2], b)

		for i in range(self.current_vertex_index):
			self.vertexes_section.vertexes[i].tangent = tangent[i]
			self.vertexes_section.vertexes[i].bitangent = bitangent[i]

	#

	def write_vertex(self, xyz, nxyz, uv):
		if self.mode == dat1lib.VERSION_RCRA:
			v = dat1lib.types.sections.model.geo.Vertex_I29.empty()
			v.x, v.y, v.z = xyz
			v.nx, v.ny, v.nz = nxyz
			if uv:
				v.u, v.v = uv
			self.vertexes_section.vertexes[self.current_vertex_index] = v
			if uv and self.uv1_section:
				self.uv1_section.set_uv(self.current_vertex_index, *uv)
		else:
			v = self.vertexes_section.vertexes[self.current_vertex_index]
			v.x, v.y, v.z = xyz
			v.nx, v.ny, v.nz = nxyz
			if uv:
				v.u, v.v = uv

		self.current_vertex_index += 1

	def write_face(self, face, vertex_offset):
		parts = face.split(" ")
		i1, i2, i3 = int(parts[0]), int(parts[1]), int(parts[2])		
		self.indexes_section.values[self.current_index_index + 0] = i3 + vertex_offset
		self.indexes_section.values[self.current_index_index + 1] = i2 + vertex_offset
		self.indexes_section.values[self.current_index_index + 2] = i1 + vertex_offset
		self.current_index_index += 3

	def get_vertex_weights(self, groups_data, weights_data):
		new_groups_data = []
		new_weights_data = []

		sum_weight = 0
		for k in range(len(groups_data)):
			if sum_weight >= 1.0:
				break
			if weights_data[k] == 0:
				continue # technically, shouldn't be any more weights then

			new_groups_data += [groups_data[k]]
			new_weights_data += [weights_data[k]]
			sum_weight += weights_data[k]

		if sum_weight > 1.0:
			new_weights_data = [w/sum_weight for w in new_weights_data]

		if len(new_weights_data) == 0:
			new_groups_data = [0]
			new_weights_data = [1.0]

		return (new_groups_data, new_weights_data)

	#

	def start_skin_batches(self, vertex_start, vertex_count):
		self.skin_batch_section.batches[self.current_skin_batch].offset = self.current_skin_offset
		self.batch_vertex_index = 0
		self.sum_batch_vertex_index = 0
		self.batch_vertex_count = vertex_count

		first_skin_batch = self.current_skin_batch
		first_weight_index = vertex_start
		return first_skin_batch, first_weight_index

	def end_skin_batches(self, first_skin_batch):
		if len(self.weights_group) > 0:
			self.write_weights_group()

		skin_batches_count = self.current_skin_batch - first_skin_batch
		return skin_batches_count

	def start_skin_batch(self):
		self.skin_batch_section.batches[self.current_skin_batch].offset = self.current_skin_offset
		self.sum_batch_vertex_index += self.batch_vertex_index
		self.batch_vertex_index = 0

	def end_skin_batch(self):
		self.skin_batch_section.batches[self.current_skin_batch].unk1 = 0 # daemon: 0x4000 for MSMR/MM?
		self.skin_batch_section.batches[self.current_skin_batch].vertex_count = self.batch_vertex_index
		self.skin_batch_section.batches[self.current_skin_batch].first_vertex = self.sum_batch_vertex_index		
		self.current_skin_batch += 1

	#

	def write_weight(self, w):
		self.weights_group += [w]
		if len(self.weights_group) < 16:
			return

		self.write_weights_group()

	def write_weights_group(self):
		groups_count = 1
		for wk in self.weights_group:
			groups_count = max(groups_count, len(wk[0]))

		self.write_skin_byte(groups_count - 1)
		for w in self.weights_group:
			if groups_count == 1:
				self.write_skin_byte(w[0][0]) # bone index				
			else:
				bone_indexes = [0] * groups_count
				weights = [0] * groups_count

				bone_indexes[0] = w[0][0]
				weights[0] = 256

				for k in range(1, len(w[0])):
					bone_indexes[k] = w[0][k]
					weights[k] = int(utils.clamp(round(w[1][k]*256.0), 0, 255))
					weights[0] -= weights[k]

				if weights[0] < 0:
					weights[0] = 0
				elif weights[0] > 255:
					weights[0] = 255
					weights[1] = 1
					bone_indexes[1] = bone_indexes[0]

				for k in range(groups_count):
					if k > 0 and weights[k] == 0:
						bone_indexes[k] = bone_indexes[k-1]
					self.write_skin_byte(bone_indexes[k])
					self.write_skin_byte(weights[k])
			self.batch_vertex_index += 1
		self.weights_group = []

		if self.sum_batch_vertex_index + self.batch_vertex_index == self.batch_vertex_count or self.batch_vertex_index == 2560:
			self.end_skin_batch()			
			self.start_skin_batch()

	def write_skin_byte(self, b):
		self.skin_section._raw[self.current_skin_offset] = b
		self.current_skin_offset += 1

	def write_rcra_weight(self, w):
		bs = [1, 0, 0, 0]
		ws = [255, 0, 0, 0]
		for j in range(min(4, len(w[0]))):
			bs[j] = w[0][j]
			ws[j] = int(utils.clamp(w[1][j]*256.0, 0, 255))

		self.rcra_weights_section.entries[self.current_rcra_weight_index] = (bs[0], bs[1], bs[2], bs[3], ws[0], ws[1], ws[2], ws[3])
		self.current_rcra_weight_index += 1

	#

	def refresh_section(self, tag):
		self.sections_to_refresh |= set([tag])

	def refresh_sections(self):
		for tag in self.sections_to_refresh:
			self.model.dat1.refresh_section_data(tag)

###

import sys

import dat1lib
import dat1lib.types.dat1
import dat1lib.types.model

###

def main(argv):
	if len(argv) < 3:
		print("Usage:")
		print("$ {} <.ascii filename> <source .model filename> [output .model filename]".format(argv[0]))
		return

	#

	ascii_fn = argv[1]
	ascii_data = None
	try:
		with open(ascii_fn, "r") as f:
			reader = AsciiReader()
			ascii_data = reader.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(ascii_fn))
		print(e)
		return

	#

	model_fn = argv[2]
	model = None
	try:
		with open(model_fn, "rb") as f:
			model = dat1lib.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(model_fn))
		print(e)
		return

	#
	
	if model is None:
		print("[!] Couldn't comprehend '{}'".format(model_fn))
		return

	if not isinstance(model, (dat1lib.types.model.Model, dat1lib.types.model.Model2, dat1lib.types.model.ModelRcra)):
		print("[!] Not a model")
		return

	#

	materials_txt = None
	if len(argv) > 3:
		materials_txt = argv[3]

	#

	injector = ModelInjector()
	injector.inject(model, ascii_data, materials_txt=materials_txt)

	#

	output_fn = model_fn + ".injected.model"
	if len(argv) > 4:
		output_fn = argv[4]

	with open(output_fn, "wb") as f:
		model.dat1.recalculate_section_headers()
		model.save(f)

if __name__ == "__main__":
	main(sys.argv)
