import dat1lib
import dat1lib.types.model
import dat1lib.types.sections.model.geo
import dat1lib.types.sections.model.meshes
import dat1lib.types.sections.model.unknowns
import dat1lib.utils as utils
import io

SECTION_INDEXES   = dat1lib.types.sections.model.geo.IndexesSection.TAG
SECTION_VERTEXES  = dat1lib.types.sections.model.geo.VertexesSection.TAG
SECTION_MESHES    = dat1lib.types.sections.model.meshes.MeshesSection.TAG
SECTION_MATERIALS = dat1lib.types.sections.model.unknowns.ModelMaterialSection.TAG

class ObjHelper(object):
	def __init__(self):
		self.cur_vertex_offset = 1
		self.cur_vt_offset = 1
		self.current_material = None
		self.mesh_vertexes = 0
		self.remembered_vertexes = []

		self.meshes_count = 0

		self.f = io.BytesIO(bytes())

	#

	def write(self, s):
		self.f.write(s.encode('ascii'))

	def start_mesh(self, mesh_name):
		self.mesh_vertexes = 0
		self.write("o {:02}_{}\n".format(self.meshes_count, mesh_name))
		self.meshes_count += 1

	def end_mesh(self):
		self.cur_vertex_offset += self.mesh_vertexes

	def write_vertex(self, x, y, z):
		def transform(x, y, z):
			return (x, y, z)

		x, y, z = transform(x, y, z)
		self.write("v {} {} {}\n".format(x, y, z))
		self.mesh_vertexes += 1

	def write_vt(self, u, v):
		self.write("vt {} {}\n".format(u, v))
		self.cur_vt_offset += 1

	def usemtl(self, mat):
		if mat != self.current_material:
			self.write("usemtl {}\n".format(mat))
			self.current_material = mat

	def write_poly(self, vs, vts):
		self.write("f {}{} {}{} {}{}\n".format(
			vs[2] + self.cur_vertex_offset, vts[2],
			vs[1] + self.cur_vertex_offset, vts[1],
			vs[0] + self.cur_vertex_offset, vts[0]
		))

	def get_output(self):
		self.f.seek(0)
		return self.f

	#

	def write_model(self, model):
		s = model.dat1.get_section(SECTION_MESHES)
		meshes = s.meshes

		s = model.dat1.get_section(SECTION_VERTEXES)
		vertexes = s.vertexes

		s = model.dat1.get_section(SECTION_INDEXES)
		indexes = s.values

		materials_section = model.dat1.get_section(SECTION_MATERIALS)

		def get_material_name(mesh):
			mat = mesh.get_material()
			material_formatted = "material{:02}".format(mat)
			
			matname = model.dat1.get_string(materials_section.string_offsets[mat][1])
			if matname is not None:
				material_formatted = matname

			return material_formatted

		#

		# pizza B3D0E63D7EA1F3E8
		# body 878B7EEABDC354A2

		for i, mesh in enumerate(meshes):
			self.start_mesh("mesh{:02}".format(i))
			self.usemtl(get_material_name(mesh))

			for vi in range(mesh.vertexStart, mesh.vertexStart + mesh.vertexCount):
				v = vertexes[vi]
				self.write_vertex(v.x, v.y, v.z)
				# TODO: v.u, v.v

			#

			faces_count = mesh.indexCount // 3
			for j in range(faces_count):
				index_index = mesh.indexStart + j*3
				deindex = mesh.indexStart
				deindex = indexes[deindex]
				deindex = 0
				self.write_poly([indexes[index_index+2]-deindex, indexes[index_index+1]-deindex, indexes[index_index]-deindex], ["", "", ""])

			self.end_mesh()

			if i > 17:
				break

		"""
		vts = ["", "", ""]
		for vt_ndx in range(len(vrtx)):
			vts[vt_ndx] = "/" + str(self.cur_vt_offset)
			self.write_vt(vt_u, vt_v)
		"""

###

def write(model):
	helper = ObjHelper()
	helper.write_model(model)
	return helper.get_output()
