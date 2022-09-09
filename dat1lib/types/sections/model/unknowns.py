import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class x7CA37DA0_Entry(object):
	def __init__(self, data):
		self.unknowns = struct.unpack("<" + "I"*12, data)

class x7CA37DA0_Section(dat1lib.types.sections.Section):
	TAG = 0x7CA37DA0
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 48
		count = len(data)//ENTRY_SIZE
		self.entries = [x7CA37DA0_Entry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def get_short_suffix(self):
		return "? ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ?            | {:6} structs".format(self.TAG, len(self.entries))

###

class x811902D7_Section(dat1lib.types.sections.Section):
	TAG = 0x811902D7
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		size1, = struct.unpack("<I", data[:4])
		self.uints = utils.read_struct_N_array_data(data[4:], size1/4 - 1, "<I")

		size2 = len(data) - size1
		self.shorts = utils.read_struct_N_array_data(data[size1:], size2/2, "<H") # includes indexes ranges where indexes go from 0 to N, where N is amount of quintuples from 0x0AD3A708

	def get_short_suffix(self):
		return "? ({}, {})".format(len(self.uints), len(self.shorts))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ?            | {:6} uints \t {:6} shorts".format(self.TAG, len(self.uints), len(self.shorts))

###

class xDCC88A19_Section(dat1lib.types.sections.Section):
	TAG = 0xDCC88A19
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.vectors = [struct.unpack("<ffff", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def get_short_suffix(self):
		return "vectors? ({})".format(len(self.vectors))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Vectors?     | {:6} vectors".format(self.TAG, len(self.vectors))
		# TODO: print vec4f

###

class xDF9FDF12_Section(dat1lib.types.sections.Section):
	TAG = 0xDF9FDF12
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<IIII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]
		# (0, 70, 0, 2)

	def get_short_suffix(self):
		return "0-70-0-2? ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 0-70-0-2?    | {:6} tuples".format(self.TAG, len(self.entries))

		if False:		
			print ""
			#######........ | 123  123456  123456  123456  123456
			print "           #         0      70       0       2"
			print "         -------------------------------------"
			for i, l in enumerate(self.entries):
				print "         - {:<3}  {:6}  {:6}  {:6}  {:6}".format(i, l[0], l[1], l[2], l[3])
			print ""

###

class xB7380E8C_Section(dat1lib.types.sections.Section):
	TAG = 0xB7380E8C
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# some unique numbers from 0, but with some gaps
		# for example, 146 numbers from 0 up to 220
		self.indexes = utils.read_struct_N_array_data(data, len(data)//2, "<H")

	def get_short_suffix(self):
		return "indexes? ({})".format(len(self.indexes))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Some Indexes | {:6} indexes".format(self.TAG, len(self.indexes))

###

class xC5354B60_Section(dat1lib.types.sections.Section): # aka model_mirror_ids
	TAG = 0xC5354B60
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# some offset-like numbers in "mostly" increasing order
		# (sometimes value returns back to a smaller number and continues to increase)
		self.offsets = utils.read_struct_N_array_data(data, len(data)//4, "<I")

	def get_short_suffix(self):
		return "offsets? ({})".format(len(self.offsets))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Some Offsets | {:6} offsets".format(self.TAG, len(self.offsets))

###

class x283D0383_Section(dat1lib.types.sections.Section): # aka model_built
	TAG = 0x283D0383
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 0x283D0383 seems to be some model info that has things like bounding box and global model scaling?
		# (global scaling is that number that is likely 0.00024. Int vertex positions are converted to floats and multiplied by this.
		self.values = utils.read_struct_N_array_data(data, len(data)//2, "<H")

	def get_short_suffix(self):
		return "model_built? ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | model_built? | {:6} shorts".format(self.TAG, len(self.values))
		print self.values
		print ""

###

class x3250BB80_Section(dat1lib.types.sections.Section): # aka model_material
	TAG = 0x3250BB80
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 16
		count = len(data) // 2 // ENTRY_SIZE
		self.string_offsets = [struct.unpack("<QQ", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]		
		# matfile, matname

		ENTRY_SIZE = 16
		data2 = data[count * ENTRY_SIZE:]
		self.triples = [struct.unpack("<QII", data2[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]
		# crc64(matfile), crc32(matname), ?

	def save(self):
		of = io.BytesIO(bytes())
		for a, b in self.string_offsets:
			of.write(struct.pack("<QQ", a, b))
		for a, b, c in self.triples:
			of.write(struct.pack("<QII", a, b, c))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "materials ({})".format(len(self.triples))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Materials    | {:6} materials".format(self.TAG, len(self.triples))

		for i, q in enumerate(self.triples):
			matfile = self._dat1.get_string(self.string_offsets[i][0])
			matname = self._dat1.get_string(self.string_offsets[i][1])

			print ""
			print "  - {:<2}  {:016X}  {}".format(i, q[0], matfile if matfile is not None else "<str at {}>".format(self.string_offsets[i][0]))
			print "        {:<8}{:08X}  {}".format(q[2], q[1], matname if matname is not None else "<str at {}>".format(self.string_offsets[i][1]))

			if config.get("section_warnings", True):
				if matfile is not None:
					real_hash = crc64.hash(matfile)
					if real_hash != q[0]:
						print "        [!] filename real hash {:016X} is not equal to one written in the struct {:016X}".format(real_hash, q[0])

				if matname is not None:
					real_hash = crc32.hash(matname)
					if real_hash != q[1]:
						print "        [!] material name real hash {:08X} is not equal to one written in the struct {:08X}".format(real_hash, q[1])
		print ""

###

class x06EB7EFC_Section(dat1lib.types.sections.Section): # aka model_look
	TAG = 0x06EB7EFC
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.values = utils.read_struct_N_array_data(data, len(data)//2, "<H")

	def get_short_suffix(self):
		return "model_look? ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | model_look?  | {:6} shorts".format(self.TAG, len(self.values))
		print self.values
		print ""

###

class x0AD3A708_Section(dat1lib.types.sections.Section):
	TAG = 0x0AD3A708
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.count, self.a, self.b, self.c = struct.unpack("<IIII", data[:16])

		rest = data[16:]
		ENTRY_SIZE = 20
		self.quintuples = [struct.unpack("<IIIII", rest[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(self.count)]
		# ?, ?, ?, ?, offset-like (small, increasing by powers of 2 (I've seen 512, 128 or 64))

	def get_short_suffix(self):
		return "? ({})".format(len(self.quintuples))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | quintuples?  | {:6} quintuples".format(self.TAG, len(self.quintuples))

		print "           {} {} {}".format(self.a, self.b, self.c)
		print ""
		#######........ | 123  12345678  12345678  12345678  12345678  123456
		print "           #           a         b         c         d  offset"
		print "         -----------------------------------------------------"
		for i, l in enumerate(self.quintuples):
			print "         - {:<3}  {:08X}  {:08X}  {:08X}  {:08X}  {:6}".format(i, l[0], l[1], l[2], l[3], l[4])
		print ""

###

class xC61B1FF5_Section(dat1lib.types.sections.Section): # aka model_skin_batch
	TAG = 0xC61B1FF5
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.a, self.b, self.c, self.data_len = struct.unpack("<IIII", data[:16])

		rest = data[16:]
		ENTRY_SIZE = 16
		count = len(rest) // ENTRY_SIZE
		self.entries = [struct.unpack("<IIHHHH", rest[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]
		# offset-like/hash, 0, 0, uncompressedSizeLike, compressedSizeLike, compressedOffsetLike

	def get_short_suffix(self):
		return "model_skin_batch? ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | skin_batch?  | {:6} structs".format(self.TAG, len(self.entries))

		print "           {} {} {}".format(self.a, self.b, self.c)
		print ""
		#######........ | 123  12345678  1234  1234  12345678  12345678  12345678
		print "           #     offset?     ?     ?       sz1       sz2       off"
		print "         -----------------------------------------------------------------"
		for i, l in enumerate(self.entries):
			print "         - {:<3}  {:8}  {:4}  {:4}  {:8}  {:8}  {:8}".format(i, l[0], l[1], l[2], l[3], l[4], l[5])
		print ""

###

class x707F1B58_Section(dat1lib.types.sections.Section):
	TAG = 0x707F1B58
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.unknown, self.data_len, self.count0, self.count1, self.count2 = struct.unpack("<IIHHI", data[:16])
		self.floats = utils.read_struct_N_array_data(data[16:], (self.data_len - 20)//4, "<f")
		self.count3, = struct.unpack("<I", data[self.data_len-4:self.data_len])
		self.shorts = []
		if len(data) > self.data_len:
			self.shorts = utils.read_struct_N_array_data(data[self.data_len:], (len(data)-self.data_len)//2, "<H")
			# unicode strings with \n??? (ends with \n\n)

	def get_short_suffix(self):
		return "? ({}, {})".format(len(self.floats), len(self.shorts))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Matrixes?    | {:6} floats, {:6} shorts".format(self.TAG, len(self.floats), len(self.shorts))
		print "           {} {} {} {} {}".format(self.unknown, self.count0, self.count1, self.count2, self.count3)
		print ""

###

class x380A5744_Section(dat1lib.types.sections.Section):
	TAG = 0x380A5744
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.unknowns = struct.unpack("<" + "I"*16, data[:4*16])
		offset = 4*16

		self.pairs = []
		# hash, offset within this section
		while offset < len(data):
			pair = struct.unpack("<Ii", data[offset:offset+8])
			offset += 8
			self.pairs += [pair]
			if pair[1] == -1:
				break

		self.pairs2 = []
		# hash, hash2 (some mapping, and usually if A->B, then B->A in this map as well)
		while offset < len(data):
			pair = struct.unpack("<II", data[offset:offset+8])
			offset += 8
			self.pairs2 += [pair]
			if pair[1] == 4294967295: # (uint)-1
				break

		self.rest = []
		if offset < len(data):
			self.rest = utils.read_struct_N_array_data(data[offset:], (len(data)-offset)//4, "<I")

	def get_short_suffix(self):
		return "? ({}, {}, {})".format(len(self.pairs), len(self.pairs2), len(self.rest))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ?            | {:6} pairs, {:6} pairs, {:6} uints".format(self.TAG, len(self.pairs), len(self.pairs2), len(self.rest))
		
		# print self.unknowns
		utils.print_table(self.unknowns, " {:8}", 4)

		print ""
		#######........ | 123  12345678  12345678
		print "           #         key     value"
		print "         -------------------------"
		for i, l in enumerate(self.pairs):
			print "         - {:<3}  {:08X}  {}".format(i, l[0], l[1])

		print ""

		#######........ | 123  12345678  12345678  123
		print "           #+        key     value  #  "
		print "         ------------------------------"
		for i, l in enumerate(self.pairs2):
			print "         - {:<3}  {:08X}  {:08X}  {:<3}".format(i+len(self.pairs), l[0], l[1], i)

		print ""

		print self.rest[:32], "..."
		print ""

###

class x4CCEA4AD_Section(dat1lib.types.sections.Section):
	TAG = 0x4CCEA4AD
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.values = [ord(c) for c in data] # usually an odd amount of bytes, WEIRD!

	def get_short_suffix(self):
		return "? ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ?            | {:6} bytes".format(self.TAG, len(self.values))

		print self.values
		print ""
