# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class x7CA37DA0_Entry(object):
	def __init__(self, data):
		self.unknowns = struct.unpack("<" + "I"*12, data)

class AmbientShadowPrimsSection(dat1lib.types.sections.Section):
	TAG = 0x7CA37DA0 # Ambient Shadow Prims
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 160 occurrences in 38298 files
		# size = 48..240 (avg = 123.9)
		#
		# examples: 808190A5B20A8431 (min size), 8007367BDC86C66B (max size)

		# MM
		# 115 occurrences in 37147 files
		# size = 48..240 (avg = 117.2)
		#
		# examples: 808190A5B20A8431 (min size), 819AC4507BA62889 (max size)

		# RCRA
		# 11 occurrences in 11387 files
		# size = 48
		#
		# examples: 903B31C97B5AE37B

		ENTRY_SIZE = 48
		count = len(data)//ENTRY_SIZE
		self.entries = [x7CA37DA0_Entry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def get_short_suffix(self):
		return "Ambient Shadow Prims ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Shadow Prims | {:6} structs".format(self.TAG, len(self.entries)))

###

class ModelBuiltSection(dat1lib.types.sections.Section):
	TAG = 0x283D0383 # Model Built
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 8780 occurrences in 8780 files (always present)
		# size = 72
		#
		# examples: 000096E6

		# MSMR
		# 38298 occurrences in 38298 files (always present)
		# size = 120
		#
		# examples: 800058C35E144B3F

		# MM
		# 37147 occurrences in 37147 files (always present)
		# size = 120
		#
		# examples: 800058C35E144B3F

		# RCRA
		# 11387 occurrences in 11387 files (always present)
		# size = 120
		#
		# examples: 800102AC251CF360

		# 0x283D0383 seems to be some model info that has things like bounding box and global model scaling?
		# (global scaling is that number that is likely 0.00024. Int vertex positions are converted to floats and multiplied by this.
		self.values = utils.read_struct_N_array_data(data, len(data)//4, "<f")

	def save(self):
		of = io.BytesIO(bytes())
		for v in self.values:
			of.write(struct.pack("<f", v))
		of.seek(0)
		return of.read()

	#

	def get_vertex_position_offset(self):
		return (self.values[0x1C//4], self.values[0x20//4], self.values[0x24//4])

	def get_vertex_position_scale(self):
		return self.values[0x2C//4]

	def get_uv_scale(self):
		iuvscale = struct.unpack("<i", struct.pack("<f", self.values[0x30//4]))[0] # TODO: don't unpack <f in the first place
		uv_scale = (1 << (iuvscale & 0xF)) / 16384.0
		return uv_scale

	def get_lod_distance(self, index):
		if index < 1 or index > 5:
			return None		
		return self.values[0x34//4 + index - 1]

	def get_indexes_count(self):
		return struct.unpack("<I", struct.pack("<f", self.values[0x64//4]))[0]

	def get_vertexes_count(self):
		return struct.unpack("<I", struct.pack("<f", self.values[0x68//4]))[0]

	#

	def get_short_suffix(self):
		return "Model Built ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Model Built  | {:6} shorts".format(self.TAG, len(self.values)))
		print(self.values)
		print("")

	def web_repr(self):
		content = "{} shorts:\n{}\n\n".format(len(self.values), self.values)
		content += "vertex_position_offset = {}\n".format(self.get_vertex_position_offset())
		
		s = self.get_vertex_position_scale()
		inv = 0
		if s > 0:
			inv = 1.0/s
		content += "vertex_position_scale  = {} (inv = {})\n".format(s, inv)

		s = self.get_uv_scale()
		inv = 0
		if s > 0:
			inv = 1.0/s
		content += "uv_scale               = {} (inv = {})\n".format(s, inv)

		content += "vertexes = {}\n".format(self.get_vertexes_count())
		content += "indexes  = {}\n".format(self.get_indexes_count())

		content += "\n"
		return {"name": "Model Built", "type": "text", "readonly": True, "content": content}

###

class ModelMaterialSection(dat1lib.types.sections.Section):
	TAG = 0x3250BB80 # Model Material
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 8775 occurrences in 8780 files
		# size = 32..1600 (avg = 68.8)
		#
		# examples: 000096E6 (min size), BC808EB3 (max size)

		# MSMR
		# 38298 occurrences in 38298 files (always present)
		# size = 32..2560 (avg = 86.6)
		#
		# examples: 800058C35E144B3F (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 37144 occurrences in 37147 files
		# size = 32..3200 (avg = 94.0)
		#
		# examples: 800058C35E144B3F (min size), 8C7796FC7478109D (max size)

		# RCRA
		# 11363 occurrences in 11387 files
		# size = 32..2976 (avg = 93.8)
		#
		# examples: 80018BF9BEE4995C (min size), 852FDCBEB5359992 (max size)

		self.version = self._dat1.version

		if self.version == dat1lib.VERSION_SO:
			ENTRY_SIZE = 32
			count = len(data) // ENTRY_SIZE

			self.string_offsets = []
			self.rest = []

			for i in range(count):
				entry = struct.unpack("<8I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])
				self.string_offsets += [(entry[0], entry[1])]
				self.rest += [(entry[2], entry[3], entry[4], entry[5], entry[6], entry[7])]

		else:
			ENTRY_SIZE = 16
			count = len(data) // 2 // ENTRY_SIZE
			self.string_offsets = [struct.unpack("<QQ", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]
			# matfile, matname

			ENTRY_SIZE = 16
			data2 = data[count * ENTRY_SIZE:]
			self.triples = [struct.unpack("<QII", data2[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]
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
		return "Model Material ({})".format(len(self.string_offsets))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Materials    | {:6} materials".format(self.TAG, len(self.string_offsets)))

		if self.version == dat1lib.VERSION_SO:
			for i, q in enumerate(self.string_offsets):
				matfile = self._dat1.get_string(self.string_offsets[i][0])
				matname = self._dat1.get_string(self.string_offsets[i][1])

				print("")
				print("  - {:<2}  {}".format(i, matfile if matfile is not None else "<str at {}>".format(self.string_offsets[i][0])))
				print("        {}".format(matname if matname is not None else "<str at {}>".format(self.string_offsets[i][1])))	

		else:
			for i, q in enumerate(self.triples):
				matfile = self._dat1.get_string(self.string_offsets[i][0])
				matname = self._dat1.get_string(self.string_offsets[i][1])

				print("")
				print("  - {:<2}  {:016X}  {}".format(i, q[0], matfile if matfile is not None else "<str at {}>".format(self.string_offsets[i][0])))
				print("        {:<8}{:08X}  {}".format(q[2], q[1], matname if matname is not None else "<str at {}>".format(self.string_offsets[i][1])))

				if config.get("section_warnings", True):
					if matfile is not None:
						real_hash = crc64.hash(matfile)
						if real_hash != q[0]:
							print("        [!] filename real hash {:016X} is not equal to one written in the struct {:016X}".format(real_hash, q[0]))

					if matname is not None:
						real_hash = crc32.hash(matname)
						if real_hash != q[1]:
							print("        [!] material name real hash {:08X} is not equal to one written in the struct {:08X}".format(real_hash, q[1]))
		
		print("")

###

class x0AD3A708_Section(dat1lib.types.sections.Section):
	TAG = 0x0AD3A708
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 3470 occurrences in 8780 files
		# size = 36..2916 (avg = 302.5)
		#
		# examples: 00755370 (min size), ABB68111 (max size)

		# MSMR
		# 2122 occurrences in 38298 files
		# size = 36..63476 (avg = 913.3)
		#
		# examples: 800804287BB19C92 (min size), BBCAFC4308D39DEC (max size)

		# MM
		# 1688 occurrences in 37147 files
		# size = 36..62656 (avg = 816.5)
		#
		# examples: 8008B62FF6E72FDE (min size), B699EAFFCD4834D0 (max size)

		# RCRA
		# 958 occurrences in 11387 files
		# size = 36..48676 (avg = 392.7)
		#
		# examples: 80116594638FB4B9 (min size), 80F95D8660F364D7 (max size)

		self.count, self.a, self.b, self.c = struct.unpack("<IIII", data[:16])

		rest = data[16:]
		ENTRY_SIZE = 20
		self.quintuples = [struct.unpack("<IIIII", rest[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(self.count)]
		# ?, ?, ?, ?, offset-like (small, increasing by powers of 2 (I've seen 512, 128 or 64))

	def get_short_suffix(self):
		return "? ({})".format(len(self.quintuples))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | quintuples?  | {:6} quintuples".format(self.TAG, len(self.quintuples)))

		print("           {} {} {}".format(self.a, self.b, self.c))
		print("")
		#######........ | 123  12345678  12345678  12345678  12345678  123456
		print("           #           a         b         c         d  offset")
		print("         -----------------------------------------------------")
		for i, l in enumerate(self.quintuples):
			print("         - {:<3}  {:08X}  {:08X}  {:08X}  {:08X}  {:6}".format(i, l[0], l[1], l[2], l[3], l[4]))
		print("")

###

class x707F1B58_Section(dat1lib.types.sections.Section):
	TAG = 0x707F1B58
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 5176 occurrences in 8780 files
		# size = 112..76048 (avg = 1134.9)
		#
		# examples: 15C0082C (min size), 7E3E18BC (max size)

		# MSMR
		# 33628 occurrences in 38298 files
		# size = 16..10752 (avg = 341.7)
		#
		# examples: 897307303895908C (min size), 8B2690F460D2A381 (max size)

		# MM
		# 33035 occurrences in 37147 files
		# size = 16..19872 (avg = 382.2)
		#
		# examples: 897307303895908C (min size), 98E8A23CBCC4635F (max size)

		# RCRA
		# 9216 occurrences in 11387 files
		# size = 160..27458 (avg = 347.2)
		#
		# examples: 800102AC251CF360 (min size), 8D14D85B15DFB268 (max size)

		"""
		self.unknown, self.data_len, self.count0, self.count1, self.count2 = struct.unpack("<IIHHI", data[:16])
		self.floats = utils.read_struct_N_array_data(data[16:], (self.data_len - 20)//4, "<f")
		self.count3, = struct.unpack("<I", data[self.data_len-4:self.data_len])
		self.shorts = []
		if len(data) > self.data_len:
			self.shorts = utils.read_struct_N_array_data(data[self.data_len:], (len(data)-self.data_len)//2, "<H")
			# unicode strings with \n??? (ends with \n\n)
		"""

	def get_short_suffix(self):		
		return "707F1B58" # return "? ({}, {})".format(len(self.floats), len(self.shorts))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		"""
		print("{:08X} | Matrixes?    | {:6} floats, {:6} shorts".format(self.TAG, len(self.floats), len(self.shorts)))
		print("           {} {} {} {} {}".format(self.unknown, self.count0, self.count1, self.count2, self.count3))
		print("")
		"""

###

class x4CCEA4AD_Section(dat1lib.types.sections.Section):
	TAG = 0x4CCEA4AD
	TYPE = 'model'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 38298 occurrences in 38298 files (always present)
		# size = 27..735 (avg = 27.6)
		#
		# examples: 800058C35E144B3F (min size), 8FCA3A1C0CF13DD0 (max size)

		# MM
		# 37147 occurrences in 37147 files (always present)
		# size = 27..745 (avg = 27.5)
		#
		# examples: 800058C35E144B3F (min size), AD7386F5F9A76C43 (max size)

		# RCRA
		# 11387 occurrences in 11387 files (always present)
		# size = 27..3875 (avg = 28.3)
		#
		# examples: 800102AC251CF360 (min size), 852FDCBEB5359992 (max size)

		self.values = [c for c in data] # usually an odd amount of bytes, WEIRD!

	def get_short_suffix(self):
		return "? ({})".format(len(self.values))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | ?            | {:6} bytes".format(self.TAG, len(self.values)))

		print(self.values)
		print("")
