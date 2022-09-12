import dat1lib
import dat1lib.types.model
import dat1lib.types.sections.model.geo
import dat1lib.types.sections.model.meshes
import dat1lib.utils as utils

SECTION_INDEXES  = dat1lib.types.sections.model.geo.IndexesSection.TAG
SECTION_VERTEXES = dat1lib.types.sections.model.geo.VertexesSection.TAG
SECTION_MESHES   = dat1lib.types.sections.model.meshes.MeshesSection.TAG

class ObjHelper(object):
	def __init__(self):
		self.cur_vertex_offset = 1
		self.cur_vt_offset = 1
		self.current_material = None
		self.mesh_vertexes = 0
		self.remembered_vertexes = []

		self.meshes_count = 0

		self.output = ""

	#

	def start_mesh(self, mesh_name):
		self.mesh_vertexes = 0
		self.output += "o {:02}_{}\n".format(self.meshes_count, mesh_name)
		self.meshes_count += 1

	def end_mesh(self):
		self.cur_vertex_offset += self.mesh_vertexes

	def write_vertex(self, x, y, z):
		def transform(x, y, z):
			return (x, y, z)

		x, y, z = transform(x, y, z)
		self.output += "v {} {} {}\n".format(x, y, z)
		self.mesh_vertexes += 1

	def write_vt(self, u, v):
		self.output += "vt {} {}\n".format(u, v)
		self.cur_vt_offset += 1

	def usemtl(self, mat):
		if mat != self.current_material:
			self.output += "usemtl {}\n".format(mat)
			self.current_material = mat

	def write_poly(self, vs, vts):
		self.output += "f {}{} {}{} {}{}\n".format(
			vs[2] + self.cur_vertex_offset, vts[2],
			vs[1] + self.cur_vertex_offset, vts[1],
			vs[0] + self.cur_vertex_offset, vts[0]
		)

	def get_output(self):
		return self.output

	#

	def write_model(self, model):
		s = model.dat1.get_section(SECTION_MESHES)
		meshes = s.meshes

		s = model.dat1.get_section(SECTION_VERTEXES)
		vertexes = s.vertexes

		s = model.dat1.get_section(SECTION_INDEXES)
		indexes = s.values

		#

		# pizza B3D0E63D7EA1F3E8
		# body 878B7EEABDC354A2

		if False:
			for v in vertexes:
				self.write_vertex(v.x, v.y, v.z)

			for i, mesh in enumerate(meshes):
				self.start_mesh("mesh{:02}".format(i))

				faces_count = mesh.indexCount // 3
				for j in xrange(mesh.indexStart, mesh.indexStart + mesh.indexCount, 3):
					self.output += "f {} {} {}\n".format(indexes[j]+1, indexes[j+1]+1, indexes[j+2]+1)

				self.end_mesh()
				break

		else:
			for i, mesh in enumerate(meshes):
				self.start_mesh("mesh{:02}".format(i))

				for vi in xrange(mesh.vertexStart, mesh.vertexStart + mesh.vertexCount):
					v = vertexes[vi]
					self.write_vertex(v.x, v.y, v.z)
					# TODO: v.u, v.v

				#

				faces_count = mesh.indexCount // 3
				for j in xrange(faces_count):
					index_index = mesh.indexStart + j*3
					deindex = mesh.indexStart
					deindex = indexes[deindex]
					self.write_poly([indexes[index_index+2]-deindex, indexes[index_index+1]-deindex, indexes[index_index]-deindex], ["", "", ""])

				self.end_mesh()

				if i > 5:
					break

		"""
		self.usemtl(new_material)

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
