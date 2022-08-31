import dat1lib.crc32 as crc32
import dat1lib.types.sections
import dat1lib.utils as utils
import io
import struct

class Event(object):
	def __init__(self, data):
		self.ulid, self.small, self.flags, self.zero, self.flags2, self.a, self.b = struct.unpack("<IHHHHHH", data)
		# a == b most of the time

class EventsSection(dat1lib.types.sections.Section):
	TAG = 0x0E19E37F
	TYPE = 'soundbank'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.events = [Event(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def get_short_suffix(self):
		return "events ({})".format(len(self.events))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Events       | {:6} events".format(self.TAG, len(self.events))
		print ""
		#######........ | 12  12345678  1234  12345  1234  12345  12345  12345
		print "           #       ulID     ?  flags  zero  flag2      ?      ?"
		print "         ------------------------------------------------------"
		for i, e in enumerate(self.events):
			print "         - {:<2}  {:08X}  {:4}  {:5}  {:4}  {:5}  {:5}  {:5}".format(i, e.ulid, e.small, e.flags, e.zero, e.flags2, e.a, e.b)

		print ""

###

class StringsSection(dat1lib.types.sections.StringsSection):
	TAG = 0x3E8490A3
	TYPE = 'soundbank'

	def __init__(self, data, container):
		dat1lib.types.sections.StringsSection.__init__(self, data, container)

	def get_short_suffix(self):
		return "strings ({})".format(len(self._strings))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Strings      | {:6} strings".format(self.TAG, len(self._strings))
		for s in self._strings:
			print " "*11 + "- '{}'".format(s)
		print ""

###

class HeaderSection(dat1lib.types.sections.Section):
	TAG = 0x4765351A
	TYPE = 'soundbank'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.a, self.b, self.bnk_section_size = struct.unpack("<HHI", data[:8])
		self.rest = data[8:]

	def get_short_suffix(self):
		return "header?"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Header?      |".format(self.TAG)
		print " "*11 + "{}  {}  {}".format(self.a, self.b, self.bnk_section_size)
		print ""
