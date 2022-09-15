import dat1lib.types.sections
import io
import struct

#

class x04C19E69_Section(dat1lib.types.sections.Section):
	TAG = 0x04C19E69
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 41 occurrences in 12274 files
		# size = 40..18176 (avg = 483.3)
		#
		# examples: 81F7066CC24960A3 (min size), B5F62C3A58DD692A (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "04C19E69 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 04C19E69     | {:6} entries".format(self.TAG, len(self.entries))

#

class x027795C5_Section(dat1lib.types.sections.Section):
	TAG = 0x027795C5
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 132 occurrences in 12274 files
		# size = 32..2352 (avg = 325.3)
		#
		# examples: 8659A59F19C88AF8 (min size), 86BC0C178D905389 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "027795C5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 027795C5     | {:6} entries".format(self.TAG, len(self.entries))

#

class x032D450A_Section(dat1lib.types.sections.Section):
	TAG = 0x032D450A
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2167 occurrences in 12274 files
		# size = 24..7080 (avg = 623.3)
		#
		# examples: 8015FB3B80A9AD40 (min size), A050B40CE45C5AFD (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "032D450A ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 032D450A     | {:6} entries".format(self.TAG, len(self.entries))

#

class x06ABCAB2_Section(dat1lib.types.sections.Section):
	TAG = 0x06ABCAB2
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 8749 occurrences in 12274 files
		# size = 160..7963760 (avg = 197793.3)
		#
		# examples: 80F452EE7C77938D (min size), A050B40CE45C5AFD (max size)
		pass

	def get_short_suffix(self):
		return "06ABCAB2 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 06ABCAB2     | {:6} bytes".format(self.TAG, len(self._raw))

#

class x041071EF_Section(dat1lib.types.sections.Section):
	TAG = 0x041071EF
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 522 occurrences in 12274 files
		# size = 2..2386 (avg = 89.6)
		#
		# examples: 8255DA1E49BCB6B8 (min size), B14ABF7C925B8777 (max size)
		pass

	def get_short_suffix(self):
		return "041071EF ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 041071EF     | {:6} bytes".format(self.TAG, len(self._raw))

#

class x24E206C8_Section(dat1lib.types.sections.Section):
	TAG = 0x24E206C8
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 651 occurrences in 12274 files
		# size = 56..938624 (avg = 39482.9)
		#
		# examples: 8018BD2AF2EBBC84 (min size), A728FA1E0C718916 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "24E206C8 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 24E206C8     | {:6} entries".format(self.TAG, len(self.entries))

#

class xA903D8F1_Section(dat1lib.types.sections.Section):
	TAG = 0xA903D8F1
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 748 occurrences in 12274 files
		# size = 348..17628828 (avg = 247433.8)
		#
		# examples: 965F8C741BC5368F (min size), 801782CA955BA5D1 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "A903D8F1 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | A903D8F1     | {:6} entries".format(self.TAG, len(self.entries))

#

class x2D1E19C6_Section(dat1lib.types.sections.Section):
	TAG = 0x2D1E19C6
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 709 occurrences in 12274 files
		# size = 66..382178 (avg = 143346.8)
		#
		# examples: B47135914B2E9941 (min size), A25699C6D1516B6B (max size)
		pass

	def get_short_suffix(self):
		return "2D1E19C6 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2D1E19C6     | {:6} bytes".format(self.TAG, len(self._raw))

#

class x1951BA1F_Section(dat1lib.types.sections.Section):
	TAG = 0x1951BA1F
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4 occurrences in 12274 files
		# size = 24..104 (avg = 64.0)
		#
		# examples: 918EE810C3239CC2 (min size), 83D5163758763E74 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "1951BA1F ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 1951BA1F     | {:6} entries".format(self.TAG, len(self.entries))

#

class x2300D240_Section(dat1lib.types.sections.Section):
	TAG = 0x2300D240
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2929 occurrences in 12274 files
		# size = 16..128176 (avg = 3318.0)
		#
		# examples: 92A2BFF3FD07FB68 (min size), 9D199DA44247F6C3 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "2300D240 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2300D240     | {:6} entries".format(self.TAG, len(self.entries))

#

class x3D8DBDB8_Section(dat1lib.types.sections.Section):
	TAG = 0x3D8DBDB8
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 12274 occurrences in 12274 files (always present)
		# size = 4
		#
		# examples: 8000DAD78C62E9FC
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "3D8DBDB8 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 3D8DBDB8     | {:6} entries".format(self.TAG, len(self.entries))

#

class x57D25F50_Section(dat1lib.types.sections.Section):
	TAG = 0x57D25F50
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 748 occurrences in 12274 files
		# size = 4..3984 (avg = 1123.5)
		#
		# examples: 84A4ACFD0558C50E (min size), AA00825BE095F0BC (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "57D25F50 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 57D25F50     | {:6} entries".format(self.TAG, len(self.entries))

#

class xD124430B_Section(dat1lib.types.sections.Section):
	TAG = 0xD124430B
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 748 occurrences in 12274 files
		# size = 176..8501936 (avg = 317525.1)
		#
		# examples: 965F8C741BC5368F (min size), 84AE7A5F3C727703 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "D124430B ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | D124430B     | {:6} entries".format(self.TAG, len(self.entries))

#

class x0CF58A6E_Section(dat1lib.types.sections.Section):
	TAG = 0x0CF58A6E
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1386 occurrences in 12274 files
		# size = 24..7512 (avg = 727.9)
		#
		# examples: 8019AC3435A8E92C (min size), 9630F216664423FD (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "0CF58A6E ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 0CF58A6E     | {:6} entries".format(self.TAG, len(self.entries))

#

class x30DADA09_Section(dat1lib.types.sections.Section):
	TAG = 0x30DADA09
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2428 occurrences in 12274 files
		# size = 16..1088 (avg = 44.3)
		#
		# examples: 800265955D8A0469 (min size), 9AF65D08D5AEA81D (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "30DADA09 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 30DADA09     | {:6} entries".format(self.TAG, len(self.entries))

#

class x17AFFFCE_Section(dat1lib.types.sections.Section):
	TAG = 0x17AFFFCE
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 417 occurrences in 12274 files
		# size = 40..41600 (avg = 2976.8)
		#
		# examples: 9075B25D1B35E0BB (min size), 8969F0889E418020 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "17AFFFCE ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 17AFFFCE     | {:6} entries".format(self.TAG, len(self.entries))

#

class x8E401376_Section(dat1lib.types.sections.Section):
	TAG = 0x8E401376
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 688 occurrences in 12274 files
		# size = 8..448 (avg = 47.6)
		#
		# examples: 8037163A9D3D35AC (min size), 8FF919F21A339FFF (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "8E401376 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 8E401376     | {:6} entries".format(self.TAG, len(self.entries))

#

class x3D5E2FEF_Section(dat1lib.types.sections.Section):
	TAG = 0x3D5E2FEF
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2611 occurrences in 12274 files
		# size = 12..516 (avg = 80.3)
		#
		# examples: 800DAB4BC4D53D50 (min size), 99600D0CB538B388 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "3D5E2FEF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 3D5E2FEF     | {:6} entries".format(self.TAG, len(self.entries))

#

class x4D7BC1C7_Section(dat1lib.types.sections.Section):
	TAG = 0x4D7BC1C7
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 6099 occurrences in 12274 files
		# size = 40..3762252 (avg = 81807.8)
		#
		# examples: 8151F22E4A189346 (min size), 9419A66DCDCE388E (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "4D7BC1C7 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 4D7BC1C7     | {:6} entries".format(self.TAG, len(self.entries))

#

class x2FFB5E42_Section(dat1lib.types.sections.Section):
	TAG = 0x2FFB5E42
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1233 occurrences in 12274 files
		# size = 8..6312 (avg = 591.5)
		#
		# examples: 8087A66DB8F99689 (min size), 974EB47F6B2CA8E3 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "2FFB5E42 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2FFB5E42     | {:6} entries".format(self.TAG, len(self.entries))

#

class x557013E9_Section(dat1lib.types.sections.Section):
	TAG = 0x557013E9
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 819 occurrences in 12274 files
		# size = 128..3712 (avg = 1024.9)
		#
		# examples: 8155973C692421D9 (min size), 86BC0C178D905389 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "557013E9 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 557013E9     | {:6} entries".format(self.TAG, len(self.entries))

#

class xCB8D34F9_Section(dat1lib.types.sections.Section):
	TAG = 0xCB8D34F9
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 688 occurrences in 12274 files
		# size = 108
		#
		# examples: 8018BD2AF2EBBC84
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "CB8D34F9 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | CB8D34F9     | {:6} entries".format(self.TAG, len(self.entries))

#

class xEDFA607D_Section(dat1lib.types.sections.Section):
	TAG = 0xEDFA607D
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 748 occurrences in 12274 files
		# size = 24..104 (avg = 101.7)
		#
		# examples: 809C68C9D8F1459B (min size), 801701AEFCE8C707 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "EDFA607D ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | EDFA607D     | {:6} entries".format(self.TAG, len(self.entries))

#

class xDC311FC3_Section(dat1lib.types.sections.Section):
	TAG = 0xDC311FC3
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 688 occurrences in 12274 files
		# size = 4..224 (avg = 23.8)
		#
		# examples: 8037163A9D3D35AC (min size), 8FF919F21A339FFF (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "DC311FC3 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | DC311FC3     | {:6} entries".format(self.TAG, len(self.entries))

#

class x50EDC53D_Section(dat1lib.types.sections.Section):
	TAG = 0x50EDC53D
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4959 occurrences in 12274 files
		# size = 32..28544 (avg = 2012.8)
		#
		# examples: 800718BAACC0D46B (min size), ACCC845E99DF7091 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "50EDC53D ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 50EDC53D     | {:6} entries".format(self.TAG, len(self.entries))

#

class xB6A0B72A_Section(dat1lib.types.sections.Section):
	TAG = 0xB6A0B72A
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 56 occurrences in 12274 files
		# size = 24..104 (avg = 88.2)
		#
		# examples: 80A4F00FD0D841EB (min size), 81CB3E8F7BCFEF97 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "B6A0B72A ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | B6A0B72A     | {:6} entries".format(self.TAG, len(self.entries))

#

class x58F861B6_Section(dat1lib.types.sections.Section):
	TAG = 0x58F861B6
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4259 occurrences in 12274 files
		# size = 4
		#
		# examples: 8000DAD78C62E9FC
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "58F861B6 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 58F861B6     | {:6} entries".format(self.TAG, len(self.entries))

#

class x5E54ACCF_Section(dat1lib.types.sections.Section):
	TAG = 0x5E54ACCF
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3374 occurrences in 12274 files
		# size = 40..648920 (avg = 6314.4)
		#
		# examples: 82E97FBB2682EEE6 (min size), 8E6D3BE864B8A163 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "5E54ACCF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 5E54ACCF     | {:6} entries".format(self.TAG, len(self.entries))

#

class x457BE3C8_Section(dat1lib.types.sections.Section):
	TAG = 0x457BE3C8
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 112 occurrences in 12274 files
		# size = 80..3200 (avg = 385.7)
		#
		# examples: 804BE6D21A712805 (min size), 92C2F69F16241F35 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "457BE3C8 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 457BE3C8     | {:6} entries".format(self.TAG, len(self.entries))

#

class x6987F172_Section(dat1lib.types.sections.Section):
	TAG = 0x6987F172
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4259 occurrences in 12274 files
		# size = 4..87680 (avg = 4338.2)
		#
		# examples: 801796BF59E439E0 (min size), A050B40CE45C5AFD (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "6987F172 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 6987F172     | {:6} entries".format(self.TAG, len(self.entries))

#

class x70682CB8_Section(dat1lib.types.sections.Section):
	TAG = 0x70682CB8
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5491 occurrences in 12274 files
		# size = 32..46880 (avg = 3370.6)
		#
		# examples: 800718BAACC0D46B (min size), 9630F216664423FD (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "70682CB8 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 70682CB8     | {:6} entries".format(self.TAG, len(self.entries))

#

class x4A07420E_Section(dat1lib.types.sections.Section):
	TAG = 0x4A07420E
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 587 occurrences in 12274 files
		# size = 12..144 (avg = 48.0)
		#
		# examples: 824007B5785E8FD5 (min size), A050B40CE45C5AFD (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "4A07420E ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 4A07420E     | {:6} entries".format(self.TAG, len(self.entries))

#

class x78684035_Section(dat1lib.types.sections.Section):
	TAG = 0x78684035
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5491 occurrences in 12274 files
		# size = 12..1260 (avg = 88.7)
		#
		# examples: 800718BAACC0D46B (min size), 880C692D52C96C16 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "78684035 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 78684035     | {:6} entries".format(self.TAG, len(self.entries))

#

class xBDAB2B0D_Section(dat1lib.types.sections.Section):
	TAG = 0xBDAB2B0D
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2562 occurrences in 12274 files
		# size = 4..216 (avg = 9.9)
		#
		# examples: 8005DF5B0745439C (min size), A0FD2DC749F10D26 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "BDAB2B0D ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | BDAB2B0D     | {:6} entries".format(self.TAG, len(self.entries))

#

class x5736A46F_Section(dat1lib.types.sections.Section):
	TAG = 0x5736A46F
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 696 occurrences in 12274 files
		# size = 16..13648 (avg = 469.9)
		#
		# examples: 843FD650B1CA2716 (min size), 94BD33EC3D9C4A0A (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "5736A46F ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 5736A46F     | {:6} entries".format(self.TAG, len(self.entries))

#

class x80D29828_Section(dat1lib.types.sections.Section):
	TAG = 0x80D29828
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3375 occurrences in 12274 files
		# size = 4..6672 (avg = 147.2)
		#
		# examples: 8101CBB169919E58 (min size), 8C3E0DAF51E24EF1 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "80D29828 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 80D29828     | {:6} entries".format(self.TAG, len(self.entries))

#

class x81999057_Section(dat1lib.types.sections.Section):
	TAG = 0x81999057
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4959 occurrences in 12274 files
		# size = 32..600556 (avg = 7038.5)
		#
		# examples: 8015DB31E416FA83 (min size), AB72D30DF307A8DF (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "81999057 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 81999057     | {:6} entries".format(self.TAG, len(self.entries))

#

class x657512BB_Section(dat1lib.types.sections.Section):
	TAG = 0x657512BB
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1233 occurrences in 12274 files
		# size = 88..69432 (avg = 6506.6)
		#
		# examples: 8087A66DB8F99689 (min size), 974EB47F6B2CA8E3 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "657512BB ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 657512BB     | {:6} entries".format(self.TAG, len(self.entries))

#

class x927C4EC3_Section(dat1lib.types.sections.Section):
	TAG = 0x927C4EC3
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2395 occurrences in 12274 files
		# size = 4..3216 (avg = 149.0)
		#
		# examples: 80796342CEE75727 (min size), 92ECCCC1029C3574 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "927C4EC3 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 927C4EC3     | {:6} entries".format(self.TAG, len(self.entries))

#

class xC6A5905E_Section(dat1lib.types.sections.Section):
	TAG = 0xC6A5905E
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 5666 occurrences in 12274 files
		# size = 12..15168 (avg = 824.2)
		#
		# examples: 800DAB4BC4D53D50 (min size), A050B40CE45C5AFD (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "C6A5905E ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | C6A5905E     | {:6} entries".format(self.TAG, len(self.entries))

#

class xDC625B3D_Section(dat1lib.types.sections.Section):
	TAG = 0xDC625B3D
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 6510 occurrences in 12274 files
		# size = 4..53416 (avg = 177.0)
		#
		# examples: 800718BAACC0D46B (min size), 9419A66DCDCE388E (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "DC625B3D ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | DC625B3D     | {:6} entries".format(self.TAG, len(self.entries))

#

class xBEAB52E7_Section(dat1lib.types.sections.Section):
	TAG = 0xBEAB52E7
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3367 occurrences in 12274 files
		# size = 12..392472 (avg = 3919.1)
		#
		# examples: 82E97FBB2682EEE6 (min size), 8E6D3BE864B8A163 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "BEAB52E7 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | BEAB52E7     | {:6} entries".format(self.TAG, len(self.entries))

#

class xC51500F1_Section(dat1lib.types.sections.Section):
	TAG = 0xC51500F1
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 4259 occurrences in 12274 files
		# size = 4
		#
		# examples: 8000DAD78C62E9FC
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "C51500F1 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | C51500F1     | {:6} entries".format(self.TAG, len(self.entries))

#

class x758BAFBD_Section(dat1lib.types.sections.Section):
	TAG = 0x758BAFBD
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 15 occurrences in 12274 files
		# size = 16..672 (avg = 100.2)
		#
		# examples: 8A435F1F8C126C1C (min size), 8A3994A8623837BD (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "758BAFBD ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 758BAFBD     | {:6} entries".format(self.TAG, len(self.entries))

#

class x97FF6EB5_Section(dat1lib.types.sections.Section):
	TAG = 0x97FF6EB5
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1563 occurrences in 12274 files
		# size = 4..5864 (avg = 524.4)
		#
		# examples: 8015DB31E416FA83 (min size), 80796342CEE75727 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "97FF6EB5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 97FF6EB5     | {:6} entries".format(self.TAG, len(self.entries))

#

class xD86A7934_Section(dat1lib.types.sections.Section):
	TAG = 0xD86A7934
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3337 occurrences in 12274 files
		# size = 32..246368 (avg = 3701.4)
		#
		# examples: 8087A66DB8F99689 (min size), 9A7DE8C86EE4E437 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "D86A7934 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | D86A7934     | {:6} entries".format(self.TAG, len(self.entries))

#

class x91DE11D9_Section(dat1lib.types.sections.Section):
	TAG = 0x91DE11D9
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1248 occurrences in 12274 files
		# size = 16..12624 (avg = 1178.2)
		#
		# examples: 8087A66DB8F99689 (min size), 974EB47F6B2CA8E3 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "91DE11D9 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 91DE11D9     | {:6} entries".format(self.TAG, len(self.entries))

#

class xEF8637D5_Section(dat1lib.types.sections.Section):
	TAG = 0xEF8637D5
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3375 occurrences in 12274 files
		# size = 4..6672 (avg = 147.2)
		#
		# examples: 8101CBB169919E58 (min size), 8C3E0DAF51E24EF1 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "EF8637D5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | EF8637D5     | {:6} entries".format(self.TAG, len(self.entries))

#

class xBCF43558_Section(dat1lib.types.sections.Section):
	TAG = 0xBCF43558
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1248 occurrences in 12274 files
		# size = 4..3156 (avg = 294.5)
		#
		# examples: 8087A66DB8F99689 (min size), 974EB47F6B2CA8E3 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "BCF43558 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | BCF43558     | {:6} entries".format(self.TAG, len(self.entries))

#

class xC4968A44_Section(dat1lib.types.sections.Section):
	TAG = 0xC4968A44
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 1386 occurrences in 12274 files
		# size = 4..272 (avg = 13.6)
		#
		# examples: 8019AC3435A8E92C (min size), 945EC47096ACEA0D (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "C4968A44 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | C4968A44     | {:6} entries".format(self.TAG, len(self.entries))

#

class xDE61C274_Section(dat1lib.types.sections.Section):
	TAG = 0xDE61C274
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2221 occurrences in 12274 files
		# size = 128..2279936 (avg = 22394.3)
		#
		# examples: 802F642EE94CF5E0 (min size), A23F7A0CCDD6C519 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "DE61C274 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | DE61C274     | {:6} entries".format(self.TAG, len(self.entries))

#

class x9CCAA06F_Section(dat1lib.types.sections.Section):
	TAG = 0x9CCAA06F
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 696 occurrences in 12274 files
		# size = 16..3461716 (avg = 117000.1)
		#
		# examples: A2804BDADA639E46 (min size), 9C187D4E0D1FB222 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "9CCAA06F ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 9CCAA06F     | {:6} entries".format(self.TAG, len(self.entries))

#

class xE4158AC3_Section(dat1lib.types.sections.Section):
	TAG = 0xE4158AC3
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2167 occurrences in 12274 files
		# size = 16..17712 (avg = 1028.3)
		#
		# examples: 8015FB3B80A9AD40 (min size), A050B40CE45C5AFD (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "E4158AC3 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | E4158AC3     | {:6} entries".format(self.TAG, len(self.entries))

#

class xF435AE9C_Section(dat1lib.types.sections.Section):
	TAG = 0xF435AE9C
	TYPE = 'Zone'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 15 occurrences in 12274 files
		# size = 48..189260 (avg = 55948.2)
		#
		# examples: BE002EABE3A3CDE1 (min size), 8A3994A8623837BD (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "F435AE9C ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | F435AE9C     | {:6} entries".format(self.TAG, len(self.entries))

