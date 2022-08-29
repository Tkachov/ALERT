import dat1lib.types.sections
import io
import struct

class MeshDefinition(object):
	def __init__(self, data):
		self.unknowns = struct.unpack("<IIIII", data[:20])
		self.vertexStart, self.indexStart, self.indexCount, self.vertexCount = struct.unpack("<IIII", data[20:36])
		self.unknowns2 = struct.unpack("<IIIIIII", data[36:])

class MeshesSection(dat1lib.types.sections.Section): # aka model_subset
	TAG = 0x78D9CBDE
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 64
		count = len(data)//ENTRY_SIZE
		self.meshes = [MeshDefinition(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for m in self.meshes:
			of.write(struct.pack("<IIIII", m.unknowns))
			of.write(struct.pack("<IIII", m.vertexStart, m.indexStart, m.indexCount, m.vertexCount))
			of.write(struct.pack("<IIIIIII", m.unknowns2))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "meshes ({})".format(len(self.meshes))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Mesh Defs    | {:6} meshes".format(self.TAG, len(self.meshes))