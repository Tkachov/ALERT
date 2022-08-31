import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class IndexesSection(dat1lib.types.sections.Section): # aka model_index
	TAG = 0x0859863D
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# Indices are weird in that instead of storing the indices directly, the indices are instead delta encoded.
		# that is, each index is a sum of the current "delta index" and all the prior delta indices.
		# For example, the true i(3) is actually di(0) + di(1) + di(2) + di(3).

		self.values = utils.read_struct_N_array_data(data, len(data)//2, "<h")

	def get_short_suffix(self):
		return "model_index ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | model_index  | {:6} shorts".format(self.TAG, len(self.values))
		print self.values[:32]

###

class VertexesSection(dat1lib.types.sections.Section): # aka model_std_vert
	TAG = 0xA98BE69B
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.values = utils.read_struct_N_array_data(data, len(data)//2, "<H")

	def get_short_suffix(self):
		return "vertexes ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Vertexes     | {:6} shorts".format(self.TAG, len(self.values))
		print self.values[:32]
