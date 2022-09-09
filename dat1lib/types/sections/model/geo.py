import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class IndexesSection(dat1lib.types.sections.Section): # aka model_index
	TAG = 0x0859863D
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 38298 occurrences in 38298 files (always present)
		# size = 6..10127496 (avg = 21726.4)
		#
		# examples: 803D66A8B5147C41 (min size), 8FCA3A1C0CF13DD0 (max size)

		self._delta_encoded = utils.read_struct_N_array_data(data, len(data)//2, "<h")
		self.values = []

		if len(self._delta_encoded) > 0:
			self.values += [self._delta_encoded[0]]

		for i in xrange(1, len(self._delta_encoded)):
			self.values += [self.values[i-1] + self._delta_encoded[i]]

	def get_short_suffix(self):
		return "model_index ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | model_index  | {:6} shorts".format(self.TAG, len(self.values))

###

class Vertex(object):
	def __init__(self, data):
		self.x, self.y, self.z, self.a, self.b, self.c = struct.unpack("<hhhHII", data)

class VertexesSection(dat1lib.types.sections.Section): # aka model_std_vert
	TAG = 0xA98BE69B
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 38298 occurrences in 38298 files (always present)
		# size = 48..17727456 (avg = 49041.9)
		# always last
		#
		# examples: 803D66A8B5147C41 (min size), 8FCA3A1C0CF13DD0 (max size)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.vertexes = [Vertex(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def get_short_suffix(self):
		return "vertexes ({})".format(len(self.vertexes))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Vertexes     | {:6} vertexes".format(self.TAG, len(self.vertexes))
		print ""
		#######........ | 123  12345678  12345678  12345678  12345678  12345678  12345678
		print "           #           x         y         z         a         b         c"
		print "         -----------------------------------------------------------------"
		for i, l in enumerate(self.vertexes[:32]):
			print "         - {:<3}  {:8}  {:8}  {:8}  {:8}  {:08X}  {:08X}".format(i, l.x, l.y, l.z, l.a, l.b, l.c)
		print "..."
		print ""

###

class x6B855EED_Section(dat1lib.types.sections.Section):
	TAG = 0x6B855EED
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1017 occurrences in 38298 files
		# size = 16..4431864 (avg = 108495.7)
		#
		# examples: 91F17B2F202041FD (min size), 8FCA3A1C0CF13DD0 (max size)

		# same amount as vertexes
		# looks like a bunch of uints
		self.values = utils.read_struct_N_array_data(data, len(data)//4, "<I")

	def get_short_suffix(self):
		return "? ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ?            | {:6} uints".format(self.TAG, len(self.values))
		print self.values[:32], "...", self.values[-32:]
		print ""

class x5CBA9DE9_Section(dat1lib.types.sections.Section):
	TAG = 0x5CBA9DE9
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 11302 occurrences in 38298 files
		# size = 16..4431864 (avg = 18953.2)
		#
		# examples: 9322A1EA95E1B12C (min size), 8FCA3A1C0CF13DD0 (max size)
		
		# same amount as vertexes
		# has a lot of 0s
		self.values = utils.read_struct_N_array_data(data, len(data)//4, "<I")

	def get_short_suffix(self):
		return "? ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ?            | {:6} uints".format(self.TAG, len(self.values))
		print self.values[:32], "...", self.values[-32:]
		#s = set(self.values)
		#print len(s), min(s), max(s)
		print ""

