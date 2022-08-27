import dat1lib.utils as utils
import dat1lib.types.sections
import io
import struct

RECALCULATE_PRESERVE_PADDING = 0
RECALCULATE_ORIGINAL_ORDER = 1
RECALCULATE_STRAIGHTFORWARD_ORDER = 2

PAD_TO = 16
EXTRA_PAD = 0

###

class DAT1SectionHeader(object):
	def __init__(self, f):
		self.tag, self.offset, self.size = utils.read_struct(f, "<III")

	@classmethod
	def make(cls, tag, offset, size):
		data = struct.pack("<III", tag, offset, size)
		f = io.BytesIO(data)
		return cls(f)

class DAT1Header(object):	
	def __init__(self, f):
		self.magic, self.unk1, self.size = utils.read_struct(f, "<III")
		self.sections = utils.read_class_array(f, "<I", DAT1SectionHeader)
		# self.sections = sorted(self.sections, key=lambda x: x.offset)

###

class DAT1(object):
	MAGIC = 0x44415431

	def __init__(self, f):
		self.header = DAT1Header(f)
		self.sections = []
		self._sections_data = []
		self._sections_map = {}

		self._recalc_strat = RECALCULATE_ORIGINAL_ORDER

		self._strings_map = {}
		self._raw_strings_data = None
		if len(self.header.sections) > 0:
			min_offset = None
			for s in self.header.sections:
				if min_offset is None or min_offset > s.offset:
					min_offset = s.offset
			self._raw_strings_data = f.read(min_offset - f.tell())
		else:
			self._raw_strings_data = f.read()

		self._read_strings(self._raw_strings_data)

		for i, s in enumerate(self.header.sections):
			f.seek(s.offset)
			self._sections_data += [f.read(s.size)]
			self._sections_map[s.tag] = i

			#print s.tag, s.offset, s.size, len(self._sections_data[-1]), repr(self._sections_data[-1][:100])

			KNOWN_SECTIONS = dat1lib.types.sections.KNOWN_SECTIONS
			if s.tag in KNOWN_SECTIONS:
				self.sections += [KNOWN_SECTIONS[s.tag](self._sections_data[-1])]
			else:
				self.sections += [None]

	def _read_strings(self, data):
		was_zero = False
		i = 0
		start = 0
		while i < len(data):
			if data[i] == '\0':
				if start == i:
					break

				s = data[start:i]
				start = i+1

			i += 1

	def get_section(self, tag):
		if tag not in self._sections_map:
			return None

		return self.sections[self._sections_map[tag]]

	def refresh_section_data(self, tag):
		if tag not in self._sections_map:
			return None

		ndx = self._sections_map[tag]
		section = self.sections[ndx]
		self._sections_data[ndx] = section.save()

	def add_section(self, tag, data):
		if tag not in self._sections_map:
			self._sections_map[tag] = len(self.sections)
			self.sections += [None]
			self._sections_data += [None]
			self.header.sections += [DAT1SectionHeader.make(tag, self.header.size, len(data))]

		ndx = self._sections_map[tag]
		self._sections_data[ndx] = data
		self.sections[ndx] = dat1lib.types.sections.KNOWN_SECTIONS[tag](data)

		self.recalculate_section_headers()

	def set_recalculation_strategy(self, strat):
		self._recalc_strat = strat

	def recalculate_section_headers(self):
		offset_to_first_section = 16 + 12 * len(self.header.sections) + len(self._raw_strings_data)
		sections_order = [s.tag for s in self.header.sections]

		if self._recalc_strat == RECALCULATE_PRESERVE_PADDING or self._recalc_strat == RECALCULATE_ORIGINAL_ORDER:
			self.header.sections = sorted(self.header.sections, key=lambda x: x.offset)
		else:
			self.header.sections = sorted(self.header.sections, key=lambda x: x.tag)

		original_padding = []
		if self._recalc_strat == RECALCULATE_PRESERVE_PADDING:
			for i in xrange(len(self.header.sections)):
				if i == 0:
					original_padding += [self.header.sections[i].offset - offset_to_first_section]
				else:
					original_padding += [self.header.sections[i].offset - (self.header.sections[i-1].offset + self.header.sections[i-1].size)]

		start = offset_to_first_section
		for i, s in enumerate(self.header.sections):
			if self._recalc_strat == RECALCULATE_PRESERVE_PADDING:
				start += original_padding[i]
			else:
				start += EXTRA_PAD
				if start % PAD_TO != 0:
					start += PAD_TO - (start % PAD_TO)
			s.offset = start
			start += len(self._sections_data[self._sections_map[s.tag]])

		self.header.size = start
		self.header.sections = sorted(self.header.sections, key=lambda x: sections_order.index(x.tag))

	def save(self, out):
		#print self.header.size
		self.recalculate_section_headers()
		#print self.header.size

		h = self.header
		out.write(struct.pack("<IIII", h.magic, h.unk1, h.size, len(h.sections)))
		for s in h.sections:
			out.write(struct.pack("<III", s.tag, s.offset, s.size))

		out.write(self._raw_strings_data)

		cur_offset = 16 + 12 * len(self.header.sections) + len(self._raw_strings_data)
		sorted_sections = [(s.tag, s.offset) for s in h.sections]
		sorted_sections = sorted(sorted_sections, key=lambda x: x[1])
		for s in sorted_sections:
			if cur_offset < s[1]:
				padding = s[1] - cur_offset
				out.write('\0' * padding)
				cur_offset += padding

			ndx = self._sections_map[s[0]]
			data = self._sections_data[ndx]
			out.write(data)
			cur_offset += len(data)
