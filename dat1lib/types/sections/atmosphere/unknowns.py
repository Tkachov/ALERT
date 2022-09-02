import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class HeaderSection(dat1lib.types.sections.Section):
	TAG = 0x02F06D4E
	TYPE = 'atmosphere'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		"""
		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.events = [Event(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]
		"""

		self.unk1 = data[:32]
		self.z1, self.time_of_day, self.z2, self.z3 = struct.unpack("<IfII", data[32:48])
		self.unk2 = data[48:64]
		self.pairs = [struct.unpack("<II", data[72+i*8:72+(i+1)*8]) for i in xrange(6)]
		self.sun_rgba = struct.unpack("<ffff", data[112:128])
		self.sun_rot, self.sun_elev = struct.unpack("<ff", data[128:136])
		self.a, self.b, self.c, self.sun_radius = struct.unpack("<IIfI", data[136:152])
		self.unk3 = struct.unpack("<" + "f"*5 + "i" + "f"*4, data[152:192])
		self.ambience_rgba = struct.unpack("<ffff", data[192:208])

	def get_short_suffix(self):
		return "header"
		# return "events ({})".format(len(self.events))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Header       |".format(self.TAG)
		print self.time_of_day
		print ["{:08X} {:08X}".format(*c) for c in self.pairs]
		print self.sun_rgba, self.sun_rot, self.sun_elev
		print self.a, self.b, self.c, self.sun_radius # "{:08X}".format(self.c)
		print self.unk3
		print self.ambience_rgba
		"""
		print ""
		#######........ | 12  12345678  1234  12345  1234  12345  12345  12345
		print "           #       ulID     ?  flags  zero  flag2      ?      ?"
		print "         ------------------------------------------------------"
		for i, e in enumerate(self.events):
			print "         - {:<2}  {:08X}  {:4}  {:5}  {:4}  {:5}  {:5}  {:5}".format(i, e.ulid, e.small, e.flags, e.zero, e.flags2, e.a, e.b)

		print ""
		"""

###

class StringsSection(dat1lib.types.sections.StringsSection):
	TAG = 0x72F28658
	TYPE = 'atmosphere'

	def __init__(self, data, container):
		dat1lib.types.sections.StringsSection.__init__(self, data, container)

	def get_short_suffix(self):
		return "strings ({})".format(len(self._strings))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Strings      | {:6} strings".format(self.TAG, len(self._strings))
		for s in self._strings:
			print " "*11 + "- '{}'".format(s)
			#print " "*13 + "{:08X} {:08X} {:016X}".format(crc32.hash(s+'\x00'), crc32.hash(s+'\x00', False), crc64.hash(s+'\x00'))
		print ""

###

class TextureSection(dat1lib.types.sections.Section):
	TAG = 0x71C168B4
	TYPE = 'atmosphere'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

	def get_short_suffix(self):
		return "texture DAT1"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Texture DAT1 |".format(self.TAG)

###

class xE7997256_Section(dat1lib.types.sections.Section):
	TAG = 0xE7997256
	TYPE = 'atmosphere'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

	def get_short_suffix(self):
		return "?"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ?            |".format(self.TAG)