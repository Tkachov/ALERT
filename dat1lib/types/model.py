import dat1lib.types.dat1
import dat1lib.utils as utils
import io
import struct

class Model(object):
	MAGIC = 0x98906B9F

	def __init__(self, f):
		self.magic, self.offset_to_stream_sections, self.stream_sections_size = struct.unpack("<III", f.read(12))
		self.unk = f.read(24)
		self._raw_dat1 = f.read()

		if self.magic != self.MAGIC:
			print "[!] Bad Model magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC)

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(self._raw_dat1), self)

	def save(self, f):
		offset_to_indexbuf = 0
		for s in self.dat1.header.sections:
			if s.tag == 0x0859863D:
				offset_to_indexbuf = s.offset

		self.offset_to_stream_sections = offset_to_indexbuf
		self.stream_sections_size = self.dat1.header.size - offset_to_indexbuf

		f.write(struct.pack("<III", self.magic, self.offset_to_stream_sections, self.stream_sections_size))
		f.write(self.unk)
		self.dat1.save(f)

	def print_info(self, config):
		print "-------"
		print "Model {:08X}".format(self.magic)
		if self.magic != self.MAGIC:
			print "[!] Unknown magic, should be {}".format(self.MAGIC)
		print ""
		print "Streaming part:"
		print "- offset = {}".format(self.offset_to_stream_sections)
		print "- size   = {}".format(self.stream_sections_size)
		if False:
			print ""
			print utils.treat_as_bytes(12, self.unk[:12])
			print utils.treat_as_bytes(12, self.unk[12:])
		print "-------"
		print ""

		self.dat1.print_info(config)

	def _get_suffix_type(self, section_header, section):
		if section_header.offset < self.offset_to_stream_sections:
			return " (info)"

		return " (streaming)"
