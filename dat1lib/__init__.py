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

SECTION_SIZE_ENTRIES = 0x65BCF461

class SizeEntry(object):
	def __init__(self, data):
		self.always1, self.value, self.index = struct.unpack("<III", data)

class SectionSizeEntries(object):
	def __init__(self, data):
		ENTRY_SIZE = 12
		count = len(data)//ENTRY_SIZE
		self.entries = [SizeEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

SECTION_ARCHIVES_MAP = 0x398ABFF0

class ArchiveFileEntry(object):
	def __init__(self, data):
		self.install_bucket, self.chunkmap = struct.unpack("<II", data[:8]) # naming according to jedijosh920
		self.filename = data[8:]

class SectionArchivesMap(object):
	def __init__(self, data):
		ENTRY_SIZE = 72
		count = len(data)//ENTRY_SIZE
		self.archives = [ArchiveFileEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

SECTION_ASSET_IDS = 0x506D7B8A

class SectionAssetIds(object):
	def __init__(self, data):
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.ids = [struct.unpack("<Q", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

SECTION_KEY_ASSETS = 0x6D921D7B

class SectionKeyAssets(object):
	def __init__(self, data):
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.ids = [struct.unpack("<Q", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

SECTION_OFFSET_ENTRIES = 0xDCD720B5

class OffsetEntry(object):
	def __init__(self, data):
		self.archive_index, self.offset = struct.unpack("<II", data)

class SectionOffsetEntries(object):
	def __init__(self, data):
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.entries = [OffsetEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

SECTION_SPAN_ENTRIES = 0xEDE8ADA9

class SpanEntry(object):
	def __init__(self, data):
		self.asset_index, self.count = struct.unpack("<II", data)

class SectionSpanEntries(object):
	def __init__(self, data):
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.entries = [SpanEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

###

KNOWN_SECTIONS = {
	SECTION_SIZE_ENTRIES: SectionSizeEntries,
	SECTION_ARCHIVES_MAP: SectionArchivesMap,
	SECTION_ASSET_IDS: SectionAssetIds,
	SECTION_KEY_ASSETS: SectionKeyAssets,
	SECTION_OFFSET_ENTRIES: SectionOffsetEntries,
	SECTION_SPAN_ENTRIES: SectionSpanEntries
}

class DAT1(object):
	def __init__(self, f, offset = 0):
		f.seek(offset)
		self.header = DAT1Header(f)
		self.sections = []
		self._sections_data = []
		self._sections_map = {}

		for i, s in enumerate(self.header.sections):
			f.seek(offset + s.offset)
			self._sections_data += [f.read(s.size)]
			self._sections_map[s.tag] = i

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

	def get_section(self, tag):
		if tag not in self._sections_map:
			return None

		return self.sections[self._sections_map[tag]]
