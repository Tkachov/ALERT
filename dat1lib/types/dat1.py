# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.decompression as decompression
import dat1lib.utils as utils
import dat1lib.types.sections
import io
import struct
import traceback

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
		sections_count, unknown_count = utils.read_struct(f, "<HH")
		self.sections = utils.read_class_N_array(f, sections_count, DAT1SectionHeader)
		self.unknowns = b""
		if unknown_count > 0:
			self.unknowns = f.read(8 * unknown_count)

	def get_offset(self):
		return 16 + 12 * len(self.sections) + len(self.unknowns)

###

class DAT1(object):
	MAGIC = 0x44415431
	EMPTY_DATA = struct.pack("<IIII", 0x44415431, 0, 16, 0)

	def __init__(self, f):
		self.header = DAT1Header(f)
		self.sections = []
		self._sections_data = []
		self._sections_map = {}

		self._recalc_strat = RECALCULATE_ORIGINAL_ORDER

		self._strings_map = {}
		self._strings_inverse_map = {}
		self._raw_strings_data = None
		if len(self.header.sections) > 0:
			min_offset = None
			for s in self.header.sections:
				if min_offset is None or min_offset > s.offset:
					min_offset = s.offset
			self._raw_strings_data = f.read(min_offset - f.tell())
		else:
			self._raw_strings_data = f.read()
		self._raw_strings_data = bytearray(self._raw_strings_data)

		self._read_strings(self._raw_strings_data)

		for i, s in enumerate(self.header.sections):
			f.seek(s.offset)
			self._sections_data += [bytearray(f.read(s.size))]
			self._sections_map[s.tag] = i

			built_section = None
			KNOWN_SECTIONS = dat1lib.types.sections.KNOWN_SECTIONS
			if s.tag in KNOWN_SECTIONS:
				try:
					built_section = KNOWN_SECTIONS[s.tag](self._sections_data[-1], self)
				except:
					built_section = Section(self._sections_data[-1], self)
			
			self.sections += [built_section]

	def _read_strings(self, data):
		was_zero = False
		i = 0
		start = 0
		while i < len(data):
			if data[i] == 0 or i == len(data)-1:
				if start == i:					
					i += 1
					start = i
					continue

				s = data[start:i].decode('utf-8')
				self._strings_map[start] = s
				self._strings_inverse_map[s] = start
				start = i+1

			i += 1

	def get_string(self, offset):
		offset -= self.header.get_offset()
		return self._strings_map.get(offset, None)

	def add_string(self, s):
		offset = self.header.get_offset()

		s = str(s)
		if s in self._strings_inverse_map:
			return offset + self._strings_inverse_map[s]

		start = len(self._raw_strings_data)
		self._strings_map[start] = s
		self._strings_inverse_map[s] = start
		self._raw_strings_data.extend(s.encode('utf-8'))
		self._raw_strings_data.extend(b'\0')
		return offset + start

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
		self.sections[ndx] = dat1lib.types.sections.KNOWN_SECTIONS[tag](data, self)

		self.recalculate_section_headers()

	def add_section_obj(self, obj):
		self.add_section_obj_with_tag(obj.TAG, obj)

	def add_section_obj_with_tag(self, tag, obj):
		if tag not in self._sections_map:
			self._sections_map[tag] = len(self.sections)
			self.sections += [None]
			self._sections_data += [None]
			self.header.sections += [DAT1SectionHeader.make(tag, self.header.size, 0)]

		ndx = self._sections_map[tag]
		self._sections_data[ndx] = bytearray(b"")
		self.sections[ndx] = obj

		self.recalculate_section_headers()

	def set_recalculation_strategy(self, strat):
		self._recalc_strat = strat

	def full_refresh(self):
		for tag in self._sections_map:
			self.refresh_section_data(tag)
		self.recalculate_section_headers()

	def recalculate_section_headers(self):
		offset_to_first_section = self.header.get_offset() + len(self._raw_strings_data)
		sections_order = [s.tag for s in self.header.sections]

		if self._recalc_strat == RECALCULATE_PRESERVE_PADDING or self._recalc_strat == RECALCULATE_ORIGINAL_ORDER:
			self.header.sections = sorted(self.header.sections, key=lambda x: x.offset)
		else:
			self.header.sections = sorted(self.header.sections, key=lambda x: x.tag)

		original_padding = []
		if self._recalc_strat == RECALCULATE_PRESERVE_PADDING:
			for i in range(len(self.header.sections)):
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
			sz = len(self._sections_data[self._sections_map[s.tag]])
			s.size = sz
			start += sz

		self.header.size = start
		self.header.sections = sorted(self.header.sections, key=lambda x: sections_order.index(x.tag))

	def save(self, out):
		self.recalculate_section_headers()

		h = self.header
		out.write(struct.pack("<IIIHH", h.magic, h.unk1, h.size, len(h.sections), len(h.unknowns)))
		sorted_sections = [(s.tag, s.offset, s.size) for s in h.sections]
		sorted_sections = sorted(sorted_sections)
		for s in sorted_sections:
			out.write(struct.pack("<III", *s))
		out.write(h.unknowns)

		out.write(self._raw_strings_data)

		cur_offset = self.header.get_offset() + len(self._raw_strings_data)
		sorted_sections = [(s.tag, s.offset) for s in h.sections]
		sorted_sections = sorted(sorted_sections, key=lambda x: x[1])
		for s in sorted_sections:
			if cur_offset < s[1]:
				padding = s[1] - cur_offset
				out.write(b'\0' * padding)
				cur_offset += padding

			ndx = self._sections_map[s[0]]
			data = self._sections_data[ndx]
			out.write(data)
			cur_offset += len(data)
