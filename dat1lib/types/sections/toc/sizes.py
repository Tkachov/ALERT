import dat1lib.types.sections
import io
import struct

class SizeEntry(object):
	def __init__(self, data):
		self.always1, self.value, self.index = struct.unpack("<III", data)

class RcraSizeEntry(object):
	def __init__(self, data):
		self.value, self.archive_index, self.offset, self.header_offset = struct.unpack("<IIIi", data)
		# value is size decompressed
		# offset is offset in archive file
		# header_offset can be -1 (probably if asset doesn't have one); offset to 36-byte header stored in the 654BDED9 (headers section)

class SizesSection(dat1lib.types.sections.Section):
	TAG = 0x65BCF461 # Archive TOC Asset Metadata
	TYPE = 'toc'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.version = self._dat1.version
		if self.version is None:
			if len(data) % 12 == 0:
				self.version = dat1lib.VERSION_MSMR
			elif len(data) % 16 == 0:
				self.version = dat1lib.VERSION_RCRA

		if self.version == dat1lib.VERSION_RCRA:
			ENTRY_SIZE = 16
			count = len(data)//ENTRY_SIZE
			self.entries = [RcraSizeEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]
		else:
			ENTRY_SIZE = 12
			count = len(data)//ENTRY_SIZE
			self.entries = [SizeEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<III", e.always1, e.value, e.index))
		of.seek(0)
		return bytearray(of.read())

	def get_short_suffix(self):
		return "sizes ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Size Entries | {:6} entries".format(self.TAG, len(self.entries)))

		if config.get("section_warnings", True):
			had_warnings = False
			if self._dat1.version == dat1lib.VERSION_SO:
				pass
			else:
				for j, e in enumerate(self.entries):
					if j != e.index:
						print("    [!] #{} bad index: {}".format(j, e.index))
						had_warnings = True
					if e.always1 != 1:
						print("    [!] #{} always1 == {}".format(j, e.always1))
						had_warnings = True
			if had_warnings:
				print("")
