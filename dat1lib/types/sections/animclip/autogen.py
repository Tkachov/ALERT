import dat1lib.types.sections
import io
import struct

#

class x09DC30AB_Section(dat1lib.types.sections.Section):
	TAG = 0x09DC30AB
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 240
		#
		# examples: 846B8D250F1A33D2
		
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
		return "09DC30AB ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 09DC30AB     | {:6} entries".format(self.TAG, len(self.entries))

#

class x1722FAEF_Section(dat1lib.types.sections.Section):
	TAG = 0x1722FAEF
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2 occurrences in 101563 files
		# size = 5712..7336 (avg = 6524.0)
		#
		# examples: 8478A801813D8B7F (min size), 9C473DAA0CFA8C46 (max size)
		
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
		return "1722FAEF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 1722FAEF     | {:6} entries".format(self.TAG, len(self.entries))

#

class x116EB684_Section(dat1lib.types.sections.Section):
	TAG = 0x116EB684
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 19529 occurrences in 101563 files
		# size = 4..109604 (avg = 2610.5)
		#
		# examples: 800348B37A689421 (min size), 9CE2AD1BCB4DB00E (max size)
		
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
		return "116EB684 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 116EB684     | {:6} entries".format(self.TAG, len(self.entries))

#

class x2BB5BC8F_Section(dat1lib.types.sections.Section):
	TAG = 0x2BB5BC8F
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 55174 occurrences in 101563 files
		# size = 4..50864 (avg = 1819.7)
		#
		# examples: 85488D6D1544D17F (min size), 9E3C7901446279A4 (max size)
		
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
		return "2BB5BC8F ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2BB5BC8F     | {:6} entries".format(self.TAG, len(self.entries))

#

class x14014CB6_Section(dat1lib.types.sections.Section):
	TAG = 0x14014CB6
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 19529 occurrences in 101563 files
		# size = 40..1560 (avg = 353.0)
		#
		# examples: 800348B37A689421 (min size), A06C251781E05522 (max size)
		
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
		return "14014CB6 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 14014CB6     | {:6} entries".format(self.TAG, len(self.entries))

#

class x1D4BD9FA_Section(dat1lib.types.sections.Section):
	TAG = 0x1D4BD9FA
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 21 occurrences in 101563 files
		# size = 80
		#
		# examples: 822F805090E0E20C
		
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
		return "1D4BD9FA ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 1D4BD9FA     | {:6} entries".format(self.TAG, len(self.entries))

#

class x3A7B4855_Section(dat1lib.types.sections.Section):
	TAG = 0x3A7B4855
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 63769 occurrences in 101563 files
		# size = 8..16548472 (avg = 11694.2)
		#
		# examples: 86A064510C89C158 (min size), 975FE295868E3A97 (max size)
		
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
		return "3A7B4855 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 3A7B4855     | {:6} entries".format(self.TAG, len(self.entries))

#

class x3976E44C_Section(dat1lib.types.sections.Section):
	TAG = 0x3976E44C
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 59909 occurrences in 101563 files
		# size = 128
		#
		# examples: 80006FCEB83F81B3
		
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
		return "3976E44C ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 3976E44C     | {:6} entries".format(self.TAG, len(self.entries))

#

class x277563F5_Section(dat1lib.types.sections.Section):
	TAG = 0x277563F5
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 10031 occurrences in 101563 files
		# size = 28..7880 (avg = 544.8)
		#
		# examples: 818633D976D7F2F7 (min size), 9CE2AD1BCB4DB00E (max size)
		
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
		return "277563F5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 277563F5     | {:6} entries".format(self.TAG, len(self.entries))

#

class x4FC98D7E_Section(dat1lib.types.sections.Section):
	TAG = 0x4FC98D7E
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 93604
		#
		# examples: 846B8D250F1A33D2
		
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
		return "4FC98D7E ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 4FC98D7E     | {:6} entries".format(self.TAG, len(self.entries))

#

class x9DF23F77_Section(dat1lib.types.sections.Section):
	TAG = 0x9DF23F77
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 101557 occurrences in 101563 files
		# size = 96
		#
		# examples: 80006FCEB83F81B3
		
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
		return "9DF23F77 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 9DF23F77     | {:6} entries".format(self.TAG, len(self.entries))

#

class x411852D5_Section(dat1lib.types.sections.Section):
	TAG = 0x411852D5
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 2 occurrences in 101563 files
		# size = 83090..9912360 (avg = 4997725.0)
		#
		# examples: 9C473DAA0CFA8C46 (min size), 8478A801813D8B7F (max size)
		pass

	def get_short_suffix(self):
		return "411852D5 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 411852D5     | {:6} bytes".format(self.TAG, len(self._raw))

#

class xA3B26640_Section(dat1lib.types.sections.Section):
	TAG = 0xA3B26640
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 55174 occurrences in 101563 files
		# size = 8..12712 (avg = 442.1)
		#
		# examples: 8004B281B238C4AB (min size), 9E3C7901446279A4 (max size)
		
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
		return "A3B26640 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | A3B26640     | {:6} entries".format(self.TAG, len(self.entries))

#

class x6962F7DE_Section(dat1lib.types.sections.Section):
	TAG = 0x6962F7DE
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 9621 occurrences in 101563 files
		# size = 32..36352 (avg = 809.9)
		#
		# examples: 8016138A3C568830 (min size), 85AA1DDD57D6B350 (max size)
		
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
		return "6962F7DE ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 6962F7DE     | {:6} entries".format(self.TAG, len(self.entries))

#

class x495BA079_Section(dat1lib.types.sections.Section):
	TAG = 0x495BA079
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 21 occurrences in 101563 files
		# size = 104..272 (avg = 216.3)
		#
		# examples: 8B02253D6E768605 (min size), 822F805090E0E20C (max size)
		
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
		return "495BA079 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 495BA079     | {:6} entries".format(self.TAG, len(self.entries))

#

class xE08AA35F_Section(dat1lib.types.sections.Section):
	TAG = 0xE08AA35F
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 59930 occurrences in 101563 files
		# size = 128..51680 (avg = 892.0)
		#
		# examples: 8000839F16C48791 (min size), 9A967494A921B89B (max size)
		
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
		return "E08AA35F ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | E08AA35F     | {:6} entries".format(self.TAG, len(self.entries))

#

class x69F64588_Section(dat1lib.types.sections.Section):
	TAG = 0x69F64588
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 10031 occurrences in 101563 files
		# size = 4..335984 (avg = 3692.1)
		#
		# examples: 841D3C3D13D24ED2 (min size), 835C8B5CA6E9FCD2 (max size)
		
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
		return "69F64588 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 69F64588     | {:6} entries".format(self.TAG, len(self.entries))

#

class x74FC0175_Section(dat1lib.types.sections.Section):
	TAG = 0x74FC0175
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 3450 occurrences in 101563 files
		# size = 4..16 (avg = 4.0)
		#
		# examples: 80006FCEB83F81B3 (min size), A7E18BFCA6DA9B17 (max size)
		
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
		return "74FC0175 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 74FC0175     | {:6} entries".format(self.TAG, len(self.entries))

#

class xD070D358_Section(dat1lib.types.sections.Section):
	TAG = 0xD070D358
	TYPE = 'AnimClip_PerformanceClip'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 22140 occurrences in 101563 files
		# size = 8..87748 (avg = 2005.7)
		#
		# examples: 802DBD52E23D275C (min size), 975FE295868E3A97 (max size)
		
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
		return "D070D358 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | D070D358     | {:6} entries".format(self.TAG, len(self.entries))

