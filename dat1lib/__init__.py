import struct
import dat1lib.utils

class DAT1SectionHeader(object):
	def __init__(self, f):
		self.tag, self.offset, self.size = utils.read_struct(f, "<III")

class DAT1Header(object):	
	def __init__(self, f):
		self.magic, self.unk1, self.size = utils.read_struct(f, "<III")
		self.sections = utils.read_class_array(f, "<I", DAT1SectionHeader)
		self.sections = sorted(self.sections, key=lambda x: x.offset)

###

class DAT1(object):
	def __init__(self, f, offset = 0):
		f.seek(offset)
		self.header = DAT1Header(f)
		self.sections_data = []
		for s in self.header.sections:
			f.seek(offset + s.offset)
			self.sections_data += [f.read(s.size)]
