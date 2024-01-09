import dat1lib
import dat1lib.types.model
import dat1lib.types.sections.model.geo
import dat1lib.types.sections.model.look
import dat1lib.types.sections.model.meshes
import dat1lib.types.sections.model.skin
import dat1lib.types.sections.model.unknowns
import struct

import base64
import io
import math
import pygltflib

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

class GltfWriter(object):
	def __init__(self):
		self.init(None)

	def init(self, model):
		self.gltf = pygltflib.GLTF2()
		self.scene = pygltflib.Scene()
		self.gltf.scenes.append(self.scene)

		self.current_node_index = 0
		self.current_mesh_index = 0
		self.current_buffer_view_index = 0
		self.current_buffer_index = 0
		self.current_accessor_index = 0
		self.binary_blob = b""

		#

		self.model = model
		self.current_vertex_index = 0

		self.mode = dat1lib.VERSION_RCRA
		if not isinstance(self.model, dat1lib.types.model.ModelRcra):
			self.mode = dat1lib.VERSION_MSMR

		self.vertexes = []
		if model is not None:
			s = model.dat1.get_section(SECTION_VERTEXES)
			self.vertexes = s.vertexes

		self.meshes = []
		if model is not None:
			s = model.dat1.get_section(SECTION_MESHES)
			self.meshes = s.meshes

		self.materials_section = None if model is None else model.dat1.get_section(SECTION_MATERIALS)
		self.uv1_section = None if model is None else model.dat1.get_section(SECTION_UV1)

		self.has_bones = None

		self.uv_scale = 1.0/16384.0
		if self.mode != dat1lib.VERSION_RCRA: # TODO: test RCRA
			s = None if model is None else model.dat1.get_section(SECTION_BUILT)
			if s:
				self.uv_scale = s.get_uv_scale()

	#

	def write_model(self, filename, model, looks, lod):
		self.init(model)

		meshes_indexes = self.get_meshes_indexes_by_looks_and_lod(looks, lod)
		skin, rcra_skin = self.get_skin()

		self.add_skeleton(model) # first, so created nodes' indexes == bones indexes
		self.add_meshes(meshes_indexes, skin, rcra_skin)

		self.gltf.save(filename)

	#

	def add_skeleton(self, model):
		joints_section = model.dat1.get_section(0x15DF9D3B)
		joints_transform_section = model.dat1.get_section(0xDCC88A19)

		bones_count = len(joints_section.joints)
		bone_indexes = [None for i in range(bones_count)]
		matrixes = []
		for i, bone in enumerate(joints_section.joints):
			name = model.dat1.get_string(bone.string_offset)
			parent = bone.parent
			pos = joints_transform_section.get_joint_position(i)
			rot = joints_transform_section.get_joint_quaternion(i)

			gltf_parent_node_index = -1
			if parent != -1:
				gltf_parent_node_index = bone_indexes[parent]

			gltf_node, gltf_node_index = self.create_node(gltf_parent_node_index)
			bone_indexes[i] = gltf_node_index

			gltf_node.name = name
			gltf_node.rotation = rot
			gltf_node.translation = pos

			matrixes += [joints_transform_section.matrixes44[i]]

		#

		matrixes_buffer_data = self.make_buffer_func(matrixes, lambda x: struct.pack("<16f", x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12], x[13], x[14], x[15]))
		matrixes_buffer_view, matrixes_buffer_view_index = self.create_buffer_view(matrixes_buffer_data, None)

		matrixes_accessor, matrixes_accessor_index = self.create_accessor()
		matrixes_accessor.bufferView = matrixes_buffer_view_index
		matrixes_accessor.byteOffset = 0
		matrixes_accessor.componentType = pygltflib.FLOAT
		matrixes_accessor.count = len(matrixes)
		matrixes_accessor.type = pygltflib.MAT4

		gltf_skin = pygltflib.Skin()
		gltf_skin.joints = bone_indexes
		gltf_skin.inverseBindMatrices = matrixes_accessor_index
		self.gltf.skins.append(gltf_skin)		

	def add_meshes(self, meshes_indexes, skin, rcra_skin):
		morph_section = self.model.dat1.get_section(0x380A5744)
		shapekeys = []
		for mi in morph_section.morph_infos:
			shapekeys += [(morph_section._dat1.get_string(mi.name_offset), mi.subset_ids)]

		for mi in meshes_indexes:
			self.add_mesh(self.make_intermediate(self.meshes[mi]), self.meshes[mi], skin, rcra_skin, mi, shapekeys)

	def make_intermediate(self, mesh):
		points = []
		normals = []
		uvs = []
		triangles = []

		# vertexes

		for vi in range(mesh.vertexStart, mesh.vertexStart + mesh.vertexCount):
			v = self.vertexes[vi]
			points += [[v.x, v.y, v.z]]
			normals += [[v.nx, v.ny, v.nz]]
			uvs += [[v.u * self.uv_scale, v.v * self.uv_scale, 0]]

		# indexes

		s = self.model.dat1.get_section(SECTION_INDEXES)
		indexes = s.values
		
		vc = mesh.vertexStart
		if (mesh.get_flags() & 0x10) > 0:
			vc = 0 # indexes are relative already

		faces_count = mesh.indexCount // 3
		for j in range(faces_count):
			index_index = mesh.indexStart + j*3
			#triangles += [[indexes[index_index+2]-vc, indexes[index_index+1]-vc, indexes[index_index]-vc]] # .ascii
			triangles += [[indexes[index_index]-vc, indexes[index_index+1]-vc, indexes[index_index+2]-vc]] # .gltf

		return (points, normals, uvs, triangles)

	def add_mesh(self, mesh, ig_mesh, skin, rcra_skin, orig_mesh_index, shapekeys):
		points, normals, uvs, triangles = mesh

		vertexes_buffer_data = self.make_buffer_func(points, lambda x: struct.pack("<3f", x[0], x[1], x[2]))
		indexes_buffer_data = self.make_buffer_func(triangles, lambda x: struct.pack("<3H", x[0], x[1], x[2]))
		normals_buffer_data = self.make_buffer_func(normals, lambda x: struct.pack("<3f", x[0], x[1], x[2]))
		uvs_buffer_data = self.make_buffer_func(uvs, lambda x: struct.pack("<2f", x[0], x[1]))

		vertexes_buffer_view, vertexes_buffer_view_index = self.create_buffer_view(vertexes_buffer_data, pygltflib.ARRAY_BUFFER)
		indexes_buffer_view, indexes_buffer_view_index = self.create_buffer_view(indexes_buffer_data, pygltflib.ELEMENT_ARRAY_BUFFER)
		normals_buffer_view, normals_buffer_view_index = self.create_buffer_view(normals_buffer_data, pygltflib.ARRAY_BUFFER)
		uvs_buffer_view, uvs_buffer_view_index = self.create_buffer_view(uvs_buffer_data, pygltflib.ARRAY_BUFFER)

		def minmax_positions(positions):
			min_x, min_y, min_z = None, None, None
			max_x, max_y, max_z = None, None, None
			for p in positions:
				x, y, z = p[0], p[1], p[2]
				if min_x is None or min_x > x:
					min_x = x
				if min_y is None or min_y > y:
					min_y = y
				if min_z is None or min_z > z:
					min_z = z
				if max_x is None or max_x < x:
					max_x = x
				if max_y is None or max_y < y:
					max_y = y
				if max_z is None or max_z < z:
					max_z = z

			return ([min_x, min_y, min_z], [max_x, max_y, max_z])

		min_ndx, max_ndx = None, None
		for t in triangles:
			for ndx in t:
				if min_ndx is None or min_ndx > ndx:
					min_ndx = ndx
				if max_ndx is None or max_ndx < ndx:
					max_ndx = ndx

		v_min, v_max = minmax_positions(points)

		vertexes_accessor, vertexes_accessor_index = self.create_accessor()
		vertexes_accessor.bufferView = vertexes_buffer_view_index
		vertexes_accessor.byteOffset = 0
		vertexes_accessor.componentType = pygltflib.FLOAT
		vertexes_accessor.count = len(points)
		vertexes_accessor.type = pygltflib.VEC3
		vertexes_accessor.min = v_min
		vertexes_accessor.max = v_max

		indexes_accessor, indexes_accessor_index = self.create_accessor()
		indexes_accessor.bufferView = indexes_buffer_view_index
		indexes_accessor.byteOffset = 0
		indexes_accessor.componentType = pygltflib.UNSIGNED_SHORT
		indexes_accessor.count = 3 * len(triangles)
		indexes_accessor.type = pygltflib.SCALAR
		indexes_accessor.min = [min_ndx]
		indexes_accessor.max = [max_ndx]

		normals_accessor, normals_accessor_index = self.create_accessor()
		normals_accessor.bufferView = normals_buffer_view_index
		normals_accessor.byteOffset = 0
		normals_accessor.componentType = pygltflib.FLOAT
		normals_accessor.count = len(normals)
		normals_accessor.type = pygltflib.VEC3

		uvs_accessor, uvs_accessor_index = self.create_accessor()
		uvs_accessor.bufferView = uvs_buffer_view_index
		uvs_accessor.byteOffset = 0
		uvs_accessor.componentType = pygltflib.FLOAT
		uvs_accessor.count = len(uvs)
		uvs_accessor.type = pygltflib.VEC2
		uvs_accessor.normalized = True # TODO: is this needed?

		primitive = pygltflib.Primitive()
		primitive.attributes.POSITION = vertexes_accessor_index
		primitive.attributes.NORMAL = normals_accessor_index
		primitive.attributes.TEXCOORD_0 = uvs_accessor_index
		primitive.indices = indexes_accessor_index

		#

		if skin is not None:
			groups_count = 4
			for vi in range(ig_mesh.vertexStart, ig_mesh.vertexStart + ig_mesh.vertexCount):
				groups_count = max(len(skin[vi]), groups_count)

			for wi in range(0, groups_count, 4):
				bufndx = wi//4
				joints_buffer = []
				weights_buffer = []

				for vi in range(ig_mesh.vertexStart, ig_mesh.vertexStart + ig_mesh.vertexCount):
					vertex = skin[vi]
					joints = []
					weights = []

					for j in range(0, 4):
						g = 0
						w = 0
						if wi + j < len(vertex):
							g, w = vertex[wi + j]
							if w == 0:
								g = 0

						joints += [g]
						weights += [w]

					joints_buffer += [joints]
					weights_buffer += [weights]

				joints_buffer_data = self.make_buffer_func(joints_buffer, lambda x: struct.pack("<4H", x[0], x[1], x[2], x[3]))
				weights_buffer_data = self.make_buffer_func(weights_buffer, lambda x: struct.pack("<4f", x[0], x[1], x[2], x[3]))

				joints_buffer_view, joints_buffer_view_index = self.create_buffer_view(joints_buffer_data, pygltflib.ARRAY_BUFFER)
				weights_buffer_view, weights_buffer_view_index = self.create_buffer_view(weights_buffer_data, pygltflib.ARRAY_BUFFER)

				joints_accessor, joints_accessor_index = self.create_accessor()
				joints_accessor.bufferView = joints_buffer_view_index
				joints_accessor.byteOffset = 0
				joints_accessor.componentType = pygltflib.UNSIGNED_SHORT
				joints_accessor.count = len(joints_buffer)
				joints_accessor.type = pygltflib.VEC4

				weights_accessor, weights_accessor_index = self.create_accessor()
				weights_accessor.bufferView = weights_buffer_view_index
				weights_accessor.byteOffset = 0
				weights_accessor.componentType = pygltflib.FLOAT
				weights_accessor.count = len(weights_buffer)
				weights_accessor.type = pygltflib.VEC4

				setattr(primitive.attributes, f"JOINTS_{bufndx}", joints_accessor_index)
				setattr(primitive.attributes, f"WEIGHTS_{bufndx}", weights_accessor_index)

		#

		gltf_mesh, gltf_mesh_index = self.create_mesh()
		gltf_mesh.primitives.append(primitive)
		gltf_mesh.name = f"sm{orig_mesh_index:02}"

		first_sk = True
		for i, sk in enumerate(shapekeys):
			sk_name, sk_subsets = sk
			if orig_mesh_index in sk_subsets:
				if first_sk:
					primitive.targets = []
					gltf_mesh.extras["targetNames"] = []
					first_sk = False

				# print(f"sm{orig_mesh_index:02} -- {sk_name}")
				self.add_shapekey(gltf_mesh, primitive, i, orig_mesh_index, len(points), len(normals))

		gltf_node, gltf_node_index = self.create_node()
		gltf_node.mesh = gltf_mesh_index
		gltf_node.skin = 0
		gltf_node.name = f"sm{orig_mesh_index:02}"

	#

	def add_shapekey(self, gltf_mesh, gltf_primitive, sk_index, subset_id, orig_vertexes_count, orig_normals_count):
		morph_section = self.model.dat1.get_section(0x380A5744)
		morph_data_section = self.model.dat1.get_section(0x5E709570)
		morph_index_section = self.model.dat1.get_section(0xA600C108)

		def from_bits(byte_list, num_bits):
			results = []
			result = 0
			bit_count = 0

			for byte in byte_list:
				for i in range(7, -1, -1):
					bit = (byte >> i) & 1
					result = (result << 1) | bit
					bit_count += 1

					if bit_count == num_bits:
						results.append(result)
						result = 0
						bit_count = 0

			if bit_count > 0:
				results.append(result)

			return results

		morph_info = morph_section.morph_infos[sk_index]
		sk_name = morph_section._dat1.get_string(morph_info.name_offset)
		
		i = morph_info.subset_ids.index(subset_id)
		if i == -1:
			return

		mi = morph_info
		if mi.packing_count >= 3:
			print(f"[!] warning: unexpected number of elements == {mi.packing_count} in shapekey '{morph_section._dat1.get_string(mi.name_offset)}'")

		positions = []
		normals = []
		indexes = []

		#for i in range(mi.subset_count):

		positions_data = []
		normals_data = []

		stride = mi.packing_count * mi.packing_bits
		offset = mi.data_offset + mi.subset_vertex_offsets[i]
		for vertexes_count, indexes_count in mi.subset_data_tables[i]:
			sz = math.ceil(stride * vertexes_count / 8.0)
			packed = morph_data_section._raw[offset:offset+sz]
			unpacked = from_bits(packed, mi.packing_bits2)

			corrected_length = len(unpacked) - (len(unpacked) % (3*mi.packing_count))

			if mi.packing_count >= 1: # read positions
				positions_data = [unpacked[i:i+3] for i in range(0, corrected_length, 3*mi.packing_count)]

			if mi.packing_count >= 2: # read normals
				normals_data = [unpacked[i+3:i+6] for i in range(0, corrected_length, 3*mi.packing_count)]

			nrml = 1.0 / (2**mi.packing_bits2)
			nrml = 1.0
			for xyz in positions_data:
				x = xyz[0]
				y = xyz[1]
				z = xyz[2]
				positions += [(x * nrml * mi.position_scale + mi.position_bias, y * nrml * mi.position_scale + mi.position_bias, z * nrml * mi.position_scale + mi.position_bias)]

			for xyz in normals_data:
				x = xyz[0]
				y = xyz[1]
				z = xyz[2]
				normals += [(x * nrml * mi.normal_scale + mi.normal_bias, y * nrml * mi.normal_scale + mi.normal_bias, z * nrml * mi.normal_scale + mi.normal_bias)]

		i = morph_info.subset_ids.index(subset_id)

		offset = mi.indexes_offset + mi.subset_index_offsets[i]
		current_index = 0
		for j, (vertexes_count, indexes_count) in enumerate(mi.subset_data_tables[i]):
			current_index = 0xA00 * j
			for k in range(indexes_count):
				skip, read = struct.unpack("<HH", morph_index_section._raw[offset:offset+4])
				offset += 4

				if read == 0:
					read = 0x20

				current_index += skip
				indexes += [current_index + ndx for ndx in range(read)]
				current_index += read

		def joined_ranges(indexes):
			if len(indexes) == 0:
				return "[]"

			result = "["
			start = indexes[0]
			end = start
			indexes = indexes[1:] + [None]
			for i in indexes:
				if i is not None and i == end+1:
					end = i
				else:
					if len(result) > 1:
						result += ", "
					result += f"{start}-{end}"
					start = i
					end = start
			result += "]"
			return result

		if False:
			if len(positions) == orig_vertexes_count:
				print(f"-- sm{subset_id:02}, {mi.packing_count}, {len(mi.subset_data_tables[i])}, {sorted(indexes) == list(range(len(indexes)))}, ranges: {joined_ranges(indexes)}")
			print(f"shapekey '{sk_name}': {len(positions)}/{len(indexes)} vertexes into {orig_vertexes_count}, min={min(indexes)}, max={max(indexes)}")

		positions_buffer = [(0,0,0) for i in range(orig_vertexes_count)]
		for i, ndx in enumerate(indexes):
			positions_buffer[ndx] = positions[i]

		normals_buffer = [(0,0,0) for i in range(orig_vertexes_count)]
		if len(normals) > 0:
			for i, ndx in enumerate(indexes):
				normals_buffer[ndx] = normals[i]

		skpos_buffer_data = self.make_buffer_func(positions_buffer, lambda x: struct.pack("<3f", x[0], x[1], x[2]))
		skpos_buffer_view, skpos_buffer_view_index = self.create_buffer_view(skpos_buffer_data, pygltflib.ARRAY_BUFFER)

		sknorm_buffer_data, sknorm_buffer_view, sknorm_buffer_view_index = None, None, None
		if len(normals) > 0:
			sknorm_buffer_data = self.make_buffer_func(normals_buffer, lambda x: struct.pack("<3f", x[0], x[1], x[2]))
			sknorm_buffer_view, sknorm_buffer_view_index = self.create_buffer_view(sknorm_buffer_data, pygltflib.ARRAY_BUFFER)

		def minmax_positions(positions):
			min_x, min_y, min_z = None, None, None
			max_x, max_y, max_z = None, None, None
			for p in positions:
				x, y, z = p[0], p[1], p[2]
				if min_x is None or min_x > x:
					min_x = x
				if min_y is None or min_y > y:
					min_y = y
				if min_z is None or min_z > z:
					min_z = z
				if max_x is None or max_x < x:
					max_x = x
				if max_y is None or max_y < y:
					max_y = y
				if max_z is None or max_z < z:
					max_z = z

			return ([min_x, min_y, min_z], [max_x, max_y, max_z])

		v_min, v_max = minmax_positions(positions_buffer)

		skpos_accessor, skpos_accessor_index = self.create_accessor()
		skpos_accessor.bufferView = skpos_buffer_view_index
		skpos_accessor.byteOffset = 0
		skpos_accessor.componentType = pygltflib.FLOAT
		skpos_accessor.count = len(positions_buffer)
		skpos_accessor.type = pygltflib.VEC3
		skpos_accessor.min = v_min
		skpos_accessor.max = v_max

		sknorm_accessor, sknorm_accessor_index = None, None
		if len(normals) > 0:
			v_min, v_max = minmax_positions(normals_buffer)

			sknorm_accessor, sknorm_accessor_index = self.create_accessor()
			sknorm_accessor.bufferView = sknorm_buffer_view_index
			sknorm_accessor.byteOffset = 0
			sknorm_accessor.componentType = pygltflib.FLOAT
			sknorm_accessor.count = len(normals_buffer)
			sknorm_accessor.type = pygltflib.VEC3
			sknorm_accessor.min = v_min
			sknorm_accessor.max = v_max

		ska = pygltflib.Attributes()
		ska.POSITION = skpos_accessor_index

		if len(normals) > 0:
			ska.NORMAL = sknorm_accessor_index

		gltf_primitive.targets += [ska]
		gltf_mesh.extras["targetNames"] += [sk_name]

	#	

	def make_buffer(self, values, struct_format):
		of = io.BytesIO(bytes())
		for v in values:
			of.write(struct.pack(struct_format, v))
		of.seek(0)
		return of.read()

	def make_buffer_func(self, values, func):
		of = io.BytesIO(bytes())
		for v in values:
			of.write(func(v))
		of.seek(0)
		return of.read()

	def create_mesh(self):
		gltf_mesh = pygltflib.Mesh()
		gltf_mesh_index = self.current_mesh_index
		self.current_mesh_index += 1
		self.gltf.meshes.append(gltf_mesh)

		return (gltf_mesh, gltf_mesh_index)

	def create_node(self, parent_node_index=-1):
		gltf_node = pygltflib.Node()
		gltf_node_index = self.current_node_index
		self.current_node_index += 1
		self.gltf.nodes.append(gltf_node)
		if parent_node_index == -1:
			self.scene.nodes.append(gltf_node_index)
		else:
			self.gltf.nodes[parent_node_index].children.append(gltf_node_index)

		return (gltf_node, gltf_node_index)

	def create_buffer_view(self, data, buffer_view_target):
		buffer = pygltflib.Buffer()
		buffer_index = self.current_buffer_index
		self.current_buffer_index += 1
		self.gltf.buffers.append(buffer)
		
		buffer_view = pygltflib.BufferView()
		buffer_view_index = self.current_buffer_view_index
		self.current_buffer_view_index += 1
		self.gltf.bufferViews.append(buffer_view)

		buffer.byteLength = len(data)

		buffer_view.buffer = buffer_index
		buffer_view.byteOffset = 0
		buffer_view.byteLength = buffer.byteLength
		if buffer_view_target is not None:
			buffer_view.target = buffer_view_target

		# self.binary_blob += data
		buffer.uri = "data:application/octet-stream;base64," + base64.b64encode(data).decode("ascii")

		return (buffer_view, buffer_view_index)

	def create_buffer_view2(self, data, buffer_view_target):
		if self.current_buffer_index == 0:
			buffer = pygltflib.Buffer()
			buffer.byteLength = 0
			buffer_index = self.current_buffer_index
			self.current_buffer_index += 1
			self.gltf.buffers.append(buffer)

		buffer = self.gltf.buffers[0]
		buffer_index = 0
		
		buffer_view = pygltflib.BufferView()
		buffer_view_index = self.current_buffer_view_index
		self.current_buffer_view_index += 1
		self.gltf.bufferViews.append(buffer_view)

		offset = buffer.byteLength
		buffer.byteLength += len(data)

		buffer_view.buffer = buffer_index
		buffer_view.byteOffset = offset
		buffer_view.byteLength = len(data)
		buffer_view.target = buffer_view_target

		self.binary_blob += data

		return (buffer_view, buffer_view_index)

	def create_accessor(self):
		gltf_accessor = pygltflib.Accessor()
		gltf_accessor_index = self.current_accessor_index
		self.current_accessor_index += 1
		self.gltf.accessors.append(gltf_accessor)

		return (gltf_accessor, gltf_accessor_index)

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

		if looks is None:
			looks = list(range(len(looks_section.looks)))

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

	def get_material_path(self, mat_index):
		matpath = self.model.dat1.get_string(self.materials_section.string_offsets[mat_index][0])
		if matpath is None:
			matpath = ""
		return matpath

###

import sys

import dat1lib
import dat1lib.types.dat1
import dat1lib.types.model

###

def main(argv):
	if len(argv) < 2:
		print("Usage:")
		print("$ {} <.model filename> [output .gltf filename]".format(argv[0]))
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

	if not isinstance(model, (dat1lib.types.model.Model, dat1lib.types.model.Model2, dat1lib.types.model.ModelRcra)):
		print("[!] Not a model")
		return

	#

	output_fn = fn + ".gltf"
	if len(argv) > 2:
		output_fn = argv[2]

	looks = [0]
	looks = None # all looks
	lod = 0
	helper = GltfWriter()
	helper.write_model(output_fn, model, looks, lod)

if __name__ == "__main__":
	main(sys.argv)
