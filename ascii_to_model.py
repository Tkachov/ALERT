import dat1lib
import dat1lib.types.model
import dat1lib.types.sections.model.geo
import dat1lib.types.sections.model.look
import dat1lib.types.sections.model.meshes
import dat1lib.types.sections.model.skin
import dat1lib.types.sections.model.unknowns
import dat1lib.utils as utils

SECTION_INDEXES     = dat1lib.types.sections.model.geo.IndexesSection.TAG
SECTION_VERTEXES    = dat1lib.types.sections.model.geo.VertexesSection.TAG
SECTION_LOOK        = dat1lib.types.sections.model.look.ModelLookSection.TAG
SECTION_MESHES      = dat1lib.types.sections.model.meshes.MeshesSection.TAG
SECTION_SKIN_BATCH  = dat1lib.types.sections.model.skin.ModelSkinBatchSection.TAG
SECTION_SKIN_DATA   = dat1lib.types.sections.model.skin.ModelSkinDataSection.TAG
SECTION_RCRA_SKIN   = dat1lib.types.sections.model.skin.xCCBAFF15_Section.TAG
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
			
			if uv_layers != 1 or textures > 1:
				print(f"mesh#{i}: unsupported uv_layers={uv_layers} or textures={textures} value!")
				return None

			self.skip(textures*2)

			vertexes = self.read_vertexes()
			faces = self.read_faces()

			meshes += [(name, uv_layers, textures, vertexes, faces)]

		return meshes

	def read_vertexes(self):
		vertexes = []

		vertexes_count = self.read_int()
		for j in range(vertexes_count):
			position = self.read_split()
			normal = self.read_split()
			color = self.read_split()
			uv = self.read_split()
			groups = self.read_split()
			weights = self.read_split()

			vertexes += [
				(
					(float(position[0]), float(position[1]), float(position[2])),
					(float(normal[0]), float(normal[1]), float(normal[2])),
					color,
					(float(uv[0]), float(uv[1])),
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

	#

	def inject(self, model, ascii_data):
		self.init(model)

		meshes_indexes = self.update_looks()
		meshes_updates = self.inject_vertexes(ascii_data, meshes_indexes)
		self.update_meshes(meshes_updates, meshes_indexes)

		self.refresh_sections()

	def update_looks(self):
		looks = [0]
		lod = 0

		#

		looks_section = self.model.dat1.get_section(SECTION_LOOK)

		s = self.model.dat1.get_section(SECTION_MESHES)
		meshes = s.meshes

		meshes_to_display = set()
		for look in looks:
			look_lod = looks_section.looks[look].lods[lod]
			meshes_to_display |= set(range(look_lod.start, look_lod.start + look_lod.count))

		meshes_indexes = []
		for i, mesh in enumerate(meshes):
			if i not in meshes_to_display:
				continue

			meshes_indexes += [i]

		#

		for look in looks:
			look_lod = looks_section.looks[look].lods[lod]
			for lod_i in range(len(looks_section.looks[look].lods)):
				if lod_i == lod:
					continue

				if looks_section.looks[look].lods[lod_i].start == 0 and looks_section.looks[look].lods[lod_i].count == 0:
					continue
				
				looks_section.looks[look].lods[lod_i].start = look_lod.start
				looks_section.looks[look].lods[lod_i].count = look_lod.count

		#

		self.refresh_section(SECTION_LOOK)

		return meshes_indexes

	def update_meshes(self, meshes_updates, meshes_indexes):
		s = self.model.dat1.get_section(SECTION_MESHES)
		meshes = s.meshes

		for i, new_mesh in enumerate(meshes_updates):
			mi = meshes_indexes[i]
			mesh = meshes[mi]
			mesh.vertexStart = new_mesh[0]
			mesh.vertexCount = new_mesh[1]
			mesh.indexStart = new_mesh[2]
			mesh.indexCount = new_mesh[3]
			mesh.first_skin_batch = new_mesh[4]
			mesh.first_weight_index = new_mesh[5]
			mesh.skin_batches_count = new_mesh[6]
			mesh.flags = mesh.flags | 0x100 # use new weights buffer

		self.refresh_section(SECTION_MESHES)

	def inject_vertexes(self, ascii_data, meshes_indexes):
		s = self.model.dat1.get_section(SECTION_MESHES)
		meshes = s.meshes

		meshes_updates = []
		for i, mesh_data in enumerate(ascii_data["meshes"]):
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
				w = self.get_vertex_weights(groups_data, weights_data)				
				self.write_vertex(xyz, nxyz, uv)
				self.write_weight(w)
				self.write_rcra_weight(w)

			mi = meshes_indexes[i]
			mesh = meshes[mi]
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

		return meshes_updates

	#

	def write_vertex(self, xyz, nxyz, uv):
		v = dat1lib.types.sections.model.geo.Vertex_I29.empty()
		v.x, v.y, v.z = xyz
		v.nx, v.ny, v.nz = nxyz
		v.u, v.v = uv
		self.vertexes_section.vertexes[self.current_vertex_index] = v
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
		self.skin_batch_section.batches[self.current_skin_batch].unk1 = 0
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
				for k in range(groups_count):
					bone_index = 0
					weight = 0

					if k < len(w[0]):
						bone_index = w[0][k]
						weight = int(utils.clamp(w[1][k]*256.0, 0, 255))

					self.write_skin_byte(bone_index)
					self.write_skin_byte(weight)			
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

	if not isinstance(model, dat1lib.types.model.ModelRcra):
		print("[!] Not a model")
		return

	#

	injector = ModelInjector()
	injector.inject(model, ascii_data)

	#

	output_fn = model_fn + ".injected.model"
	if len(argv) > 3:
		output_fn = argv[3]

	with open(output_fn, "wb") as f:
		model.dat1.recalculate_section_headers()
		model.save(f)

if __name__ == "__main__":
	main(sys.argv)
