import struct
import dat1lib.utils
import json
import io

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

SECTION_SIZE_ENTRIES = 0x65BCF461

class SizeEntry(object):
	def __init__(self, data):
		self.always1, self.value, self.index = struct.unpack("<III", data)

class SectionSizeEntries(object):
	def __init__(self, data):
		ENTRY_SIZE = 12
		count = len(data)//ENTRY_SIZE
		self.entries = [SizeEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<III", e.always1, e.value, e.index))
		of.seek(0)
		return of.read()

SECTION_ARCHIVES_MAP = 0x398ABFF0

class ArchiveFileEntry(object):
	def __init__(self, data):
		self.install_bucket, self.chunkmap = struct.unpack("<II", data[:8]) # naming according to jedijosh920
		self.filename = data[8:]

	@classmethod
	def make(cls, bucket, chunk, filename):
		data = struct.pack("<II", bucket, chunk)
		f = io.BytesIO()# data)
		f.write(data)
		f.write(filename)
		if len(filename) < 64:
			f.write('\0' * (64 - len(filename)))
		f.seek(0)
		return cls(f.read())

class SectionArchivesMap(object):
	def __init__(self, data):
		ENTRY_SIZE = 72
		count = len(data)//ENTRY_SIZE
		self.archives = [ArchiveFileEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.archives:
			of.write(struct.pack("<II", e.install_bucket, e.chunkmap))
			of.write(e.filename)
		of.seek(0)
		return of.read()

SECTION_ASSET_IDS = 0x506D7B8A

class SectionAssetIds(object):
	def __init__(self, data):
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.ids = [struct.unpack("<Q", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for aid in self.ids:
			of.write(struct.pack("<Q", aid))
		of.seek(0)
		return of.read()

SECTION_KEY_ASSETS = 0x6D921D7B

class SectionKeyAssets(object):
	def __init__(self, data):
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.ids = [struct.unpack("<Q", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for aid in self.ids:
			of.write(struct.pack("<Q", aid))
		of.seek(0)
		return of.read()

SECTION_OFFSET_ENTRIES = 0xDCD720B5

class OffsetEntry(object):
	def __init__(self, data):
		self.archive_index, self.offset = struct.unpack("<II", data)

class SectionOffsetEntries(object):
	def __init__(self, data):
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.entries = [OffsetEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<II", e.archive_index, e.offset))
		of.seek(0)
		return of.read()

SECTION_SPAN_ENTRIES = 0xEDE8ADA9

class SpanEntry(object):
	def __init__(self, data):
		self.asset_index, self.count = struct.unpack("<II", data)

class SectionSpanEntries(object):
	def __init__(self, data):
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.entries = [SpanEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

SECTION_MOD = 0x30444F4D

class SectionMod(object):
	def __init__(self, data):
		self.data = json.loads(data)

	def __str__(self):
		return "{}".format(self.data)

###

KNOWN_SECTIONS = {
	SECTION_SIZE_ENTRIES: SectionSizeEntries,
	SECTION_ARCHIVES_MAP: SectionArchivesMap,
	SECTION_ASSET_IDS: SectionAssetIds,
	SECTION_KEY_ASSETS: SectionKeyAssets,
	SECTION_OFFSET_ENTRIES: SectionOffsetEntries,
	SECTION_SPAN_ENTRIES: SectionSpanEntries,
	SECTION_MOD: SectionMod
}

class DAT1(object):
	def __init__(self, f, offset = 0):
		f.seek(offset)
		self.header = DAT1Header(f)
		self.sections = []
		self._sections_data = []
		self._sections_map = {}

		self._strings_map = {}
		self._raw_strings_data = None
		if len(self.header.sections) > 0:
			# self._raw_strings_data = f.read(self.header.sections[0].offset - f.tell())
			min_offset = None
			for s in self.header.sections:
				if min_offset is None or min_offset > s.offset:
					min_offset = s.offset
			self._raw_strings_data = f.read(min_offset - f.tell())
		else:
			self._raw_strings_data = f.read()
		#print len(self._raw_strings_data)

		self._read_strings(self._raw_strings_data)

		for i, s in enumerate(self.header.sections):
			f.seek(offset + s.offset)
			self._sections_data += [f.read(s.size)]
			self._sections_map[s.tag] = i

			#print s.tag, s.offset, s.size, len(self._sections_data[-1]), repr(self._sections_data[-1][:100])

			if s.tag in KNOWN_SECTIONS:
				self.sections += [KNOWN_SECTIONS[s.tag](self._sections_data[-1])]
			else:
				self.sections += [None]

			"""
			if s.tag == SECTION_SIZE_ENTRIES:
				self.sections += [SectionSizeEntries(self._sections_data[-1])]
			else:
				self.sections += [None]
			"""

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
		self.sections[ndx] = KNOWN_SECTIONS[tag](data)

		self.recalculate_section_headers()

	def recalculate_section_headers(self):
		offset_to_first_section = 16 + 12 * len(self.header.sections) + len(self._raw_strings_data)
		sections_order = [s.tag for s in self.header.sections]
		"""
		print sections_order
		for s in self.header.sections:
			print s.tag, s.offset
		"""

		self.header.sections = sorted(self.header.sections, key=lambda x: x.offset)

		start = offset_to_first_section
		for s in self.header.sections:
			s.offset = start
			start += len(self._sections_data[self._sections_map[s.tag]])
			if start % 16 != 0:
				start += 16 - (start % 16)

		self.header.size = start
		self.header.sections = sorted(self.header.sections, key=lambda x: sections_order.index(x.tag))
		"""
		for s in self.header.sections:
			print s.tag, s.offset
		"""

	def save(self, out):
		#print self.header.size
		self.recalculate_section_headers()
		#print self.header.size

		h = self.header
		out.write(struct.pack("<IIII", h.magic, h.unk1, h.size, len(h.sections)))
		for s in h.sections:
			out.write(struct.pack("<III", s.tag, s.offset, s.size))

		out.write(self._raw_strings_data)

		"""
		for s in self._sections_data:
			out.write(s)
		"""
		cur_offset = 16 + 12 * len(self.header.sections) + len(self._raw_strings_data)	
		sorted_sections = [(s.tag, s.offset) for s in h.sections]
		sorted_sections = sorted(sorted_sections, key=lambda x: x[1])
		for s in sorted_sections:
			ndx = self._sections_map[s[0]]
			data = self._sections_data[ndx]
			out.write(data)
			cur_offset += len(data)
			if cur_offset % 16 != 0:
				padding = 16 - (cur_offset % 16)
				out.write('\0' * padding)
				cur_offset += padding
