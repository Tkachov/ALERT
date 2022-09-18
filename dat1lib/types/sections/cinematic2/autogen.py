import dat1lib.types.sections
import io
import struct

class x0A231B40_Section(dat1lib.types.sections.Section):
	TAG = 0x0A231B40
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 16..1072 (avg = 95.9)
		#
		# examples: 8003278FC28C9C4B (min size), A8A79439EA51466A (max size)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<QII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

		# same Q as in 0xF59A5B54, also the same amount of entries

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "0A231B40 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 0A231B40     | {:6} entries".format(self.TAG, len(self.entries))
		for i, x in enumerate(self.entries):
			print "  - {:<3}  {:016X} {:4} {:4}".format(i, x[0], x[1], x[2])
		print ""

#

class x0CDE73EF_Section(dat1lib.types.sections.Section):
	TAG = 0x0CDE73EF
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 8..912 (avg = 147.5)
		#
		# examples: 845FE1CCB4A2873B (min size), 98B019CCD404CC37 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<HBB", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def get_short_suffix(self):
		return "0CDE73EF ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 0CDE73EF     | {:6} entries".format(self.TAG, len(self.entries))
		if True:
			for i, x in enumerate(self.entries):
				print "  - {:<3}  {:3} {:3} {:3}".format(i, *x)
			print ""

#

class x13AAEFE2_Section(dat1lib.types.sections.Section):
	TAG = 0x13AAEFE2
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 24..1608 (avg = 143.9)
		#
		# examples: 8003278FC28C9C4B (min size), A8A79439EA51466A (max size)
		
		ENTRY_SIZE = 24
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<IIIhhhhhh", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "13AAEFE2 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 13AAEFE2     | {:6} entries".format(self.TAG, len(self.entries))
		for i, x in enumerate(self.entries):
			print "  - {:<3}  {:08X} {:08X} {:5} {:3} {:3} {:3} {:3} {:3} {:3}".format(i, *x)
		print ""

#

class x15C2983A_Section(dat1lib.types.sections.Section):
	TAG = 0x15C2983A
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 458 occurrences in 724 files
		# size = 36..171341 (avg = 9374.7)
		#
		# examples: AF299BDA906DC7CA (min size), A8A79439EA51466A (max size)

		self.cnt1, self.cnt2, self.cnt3, self.cnt4 = struct.unpack("<HHHH", data[:8])

		rest = data[8:]
		ENTRY_SIZE = 40
		self.entries1 = [struct.unpack("<IIIIIIIIII", rest[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(self.cnt1)]

		rest = data[8+ENTRY_SIZE*self.cnt1:]
		ENTRY_SIZE = 24
		self.entries2 = [struct.unpack("<IIIIHHHH", rest[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(self.cnt2)]

		self.rest = rest[ENTRY_SIZE*self.cnt2:]

	def get_short_suffix(self):
		return "15C2983A ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 15C2983A     | {:6} bytes".format(self.TAG, len(self._raw))
		if True: # False:
			print self.cnt1, self.cnt2, self.cnt3, self.cnt4
			print ""
			for i, x in enumerate(self.entries1):
				# print "  - {:<3}  {}".format(i, x)
				print "  - {:<3}  {:08X} {:08X} {:08X} {:08X} {:08X} {:08X} {:4} {:4} {:08X} {:4}".format(i, *x)				
			print ""
			for i, x in enumerate(self.entries2):
				# print "  - {:<3}  {}".format(i, x)
				print "  - {:<3}  {:08X} {:08X} {:08X} {:4} {:4} {:4} {:4} {:4}".format(i, *x)
			print ""
			print len(self.rest)
			print ""

#

class x2029471C_Section(dat1lib.types.sections.Section):
	TAG = 0x2029471C
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 269 occurrences in 724 files
		# size = 12..17160 (avg = 1467.3)
		#
		# examples: 8B12BE5D2364E4F9 (min size), A0D237BF807F8B9F (max size)
		
		ENTRY_SIZE = 12
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<IIHH", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def get_short_suffix(self):
		return "2029471C ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2029471C     | {:6} entries".format(self.TAG, len(self.entries))
		for i, x in enumerate(self.entries):
			print "  - {:<3}  {:08X} {:4} {:4} {:4}".format(i, *x)
		print ""

#

class x26AB8388_Section(dat1lib.types.sections.Section):
	TAG = 0x26AB8388
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 24..94792 (avg = 2611.6)
		#
		# examples: 82B8360A1DEAFDFD (min size), A8A79439EA51466A (max size)

		self.headers = []
		self.values = []

		i = 0
		while i < len(data):
			a, b, c = struct.unpack("<Ihh", data[i:i+8])
			if a >= len(data):
				break

			i += 8
			self.headers += [(a, b, c)]

		for h in self.headers:
			a, b, c = h
			rest = data[a:]

			ENTRY_SIZE = 16
			self.values += [[struct.unpack("<QhhI", rest[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(c)]]
			# sorted by e[0]

	def get_short_suffix(self):
		return "26AB8388 ({})".format(len(self.headers))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 26AB8388     | {:6} headers".format(self.TAG, len(self.headers))
		for i, h in enumerate(self.headers):
			print ""
			print "  - {:<3} {:4} {:4} {:4}".format(i, *h)
			for j, e in enumerate(self.values[i]):
				print "         - {:<3}  {:016X} {:4} {:4} {:4}".format(j, *e)
		print ""

#

class x2D9B0A30_Section(dat1lib.types.sections.Section):
	TAG = 0x2D9B0A30
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 580 occurrences in 724 files
		# size = 30..248520 (avg = 7067.7)
		#
		# examples: 9293876A1ACBBA8D (min size), A0D237BF807F8B9F (max size)
		pass

	def get_short_suffix(self):
		return "2D9B0A30 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2D9B0A30     | {:6} bytes".format(self.TAG, len(self._raw))
		print " ".join(["{:02X}".format(ord(c)) for c in self._raw])

#

class x2F161636_Section(dat1lib.types.sections.Section):
	TAG = 0x2F161636
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 8..536 (avg = 47.9)
		#
		# examples: 8003278FC28C9C4B (min size), A8A79439EA51466A (max size)
		
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<fI", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

		# k - seems like a small increasing float number -- maybe time in seconds?
		# v - index of Q from 0xF59A5B54 in 0x0A231B40
		# for example:
		#
		# i k        v
		# 0 00000000 0
		# 1 405BBBBE 2
		# 2 40B9999C 4
		# 3 40F33336 1
		# 4 41255557 3
		#
		# here, v=4 (when i=2) means that 0xF59A5B54[2] == 0x0A231B40[4]
		#
		# same amount of entries as in 0x0A231B40, 0xF59A5B54

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "2F161636 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2F161636     | {:6} entries".format(self.TAG, len(self.entries))
		for i, (k, v) in enumerate(self.entries):
			print "  - {:<3}  {} {}".format(i, k, v)
		print ""

#

class x2EF690BD_Section(dat1lib.types.sections.Section):
	TAG = 0x2EF690BD
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 269 occurrences in 724 files
		# size = 2..134 (avg = 23.7)
		#
		# examples: 89A71B7F8F42C1E5 (min size), A8A79439EA51466A (max size)
		ENTRY_SIZE = 2
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<H", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def get_short_suffix(self):
		return "2EF690BD ({} values)".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2EF690BD     | {:6} values".format(self.TAG, len(self.entries))
		for i, x in enumerate(self.entries):
			print "  - {:<3}  {:3}".format(i, x)

#

class x34E97238_Section(dat1lib.types.sections.Section):
	TAG = 0x34E97238
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 144..4152 (avg = 329.6)
		#
		# examples: 8D46E415B4F7FECA (min size), A8A79439EA51466A (max size)
		
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
		return "34E97238 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 34E97238     | {:6} entries".format(self.TAG, len(self.entries))
		"""
		for i, x in enumerate(self.entries):
			a, b = struct.unpack("<hh", struct.pack("<I", x))
			c, = struct.unpack("<f", struct.pack("<I", x))
			print "  - {:<3}  {:08X} {:10} {:6} {:6} {}".format(i, x, x, a, b, c)
		print ""
		"""

#

class x5BE2A972_Section(dat1lib.types.sections.Section):
	TAG = 0x5BE2A972
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 32..11488 (avg = 575.7)
		#
		# examples: 8D46E415B4F7FECA (min size), A8A79439EA51466A (max size)
		
		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<QII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]
		# sorted by e[0]

	def get_short_suffix(self):
		return "5BE2A972 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 5BE2A972     | {:6} entries".format(self.TAG, len(self.entries))
		for i, x in enumerate(self.entries):
			print "  - {:<3}  {:016X} {:4} {}".format(i, *x)
		print ""

#

class x85272DB0_Section(dat1lib.types.sections.Section):
	TAG = 0x85272DB0
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 248..393072 (avg = 22471.1)
		#
		# examples: B82D0A801D7E99A4 (min size), A8A79439EA51466A (max size)
		
		# take offsets from 0xADCF5096 and read

	def get_short_suffix(self):
		return "85272DB0 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		self.values = []
		s = self._dat1.get_section(0xADCF5096)
		offs = [off for _, _, off, _ in s.entries]
		offs = sorted(offs)
		for i in xrange(len(offs)):
			self.values += [self._raw[offs[i]:offs[i+1] if i != len(offs)-1 else -1]]

		# serialized similarly to SerializedSection? (but different, other type marks and no header)

		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 85272DB0     | {:6} bytes".format(self.TAG, len(self._raw))
		if False:
			for i, v in enumerate(self.values):
				print "  - {:<3}  {:6}  {}".format(i, len(v), " ".join("{:02X}".format(ord(c)) for c in v))
			print ""

#

class x7EF72163_Section(dat1lib.types.sections.Section):
	TAG = 0x7EF72163
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 269 occurrences in 724 files
		# size = 24..156 (avg = 26.5)
		#
		# examples: 800D2F7E5B7F5D65 (min size), 848B35DDF0C461B6 (max size)
		
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
		return "7EF72163 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 7EF72163     | {:6} entries".format(self.TAG, len(self.entries))
		for i, x in enumerate(self.entries):
			print "  - {:<3}  {:08X} {}".format(i, x, x)
		print ""

#

class x802A0575_Section(dat1lib.types.sections.Section):
	TAG = 0x802A0575
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 269 occurrences in 724 files
		# size = 448..45776 (avg = 10874.4)
		#
		# examples: B26A6BACA101C902 (min size), 98B019CCD404CC37 (max size)
		
		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<II", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "802A0575 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 802A0575     | {:6} entries".format(self.TAG, len(self.entries))
		if False:
			for i, x in enumerate(self.entries):
				print "  - {:<3}  {:8} {}".format(i, x[0], x[1])
			print ""

#

class xA20AD331_Section(dat1lib.types.sections.Section):
	TAG = 0xA20AD331
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 587 occurrences in 724 files
		# size = 64..7296 (avg = 1232.7)
		#
		# examples: 9AA0719D4FB56E3E (min size), 98B019CCD404CC37 (max size)
		
		ENTRY_SIZE = 32
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<QQQII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

	def get_short_suffix(self):
		return "A20AD331 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | A20AD331     | {:6} entries".format(self.TAG, len(self.entries))
		for i, x in enumerate(self.entries):
			print "  - {:<3}  {:016X} {:016X} {:016X} {} {}".format(i, *x)
		print ""

#

class xADCF5096_Section(dat1lib.types.sections.Section):
	TAG = 0xADCF5096
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 72..76080 (avg = 3914.2)
		#
		# examples: 8D46E415B4F7FECA (min size), A0D237BF807F8B9F (max size)
		
		ENTRY_SIZE = 24
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<QQII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

		# sorted by e[0]
		# e[1] -- also met in 0x5BE2A972, 0x26AB8388
		# e[2] -- offset to something in 0x85272DB0, probably

	def get_short_suffix(self):
		return "ADCF5096 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ADCF5096     | {:6} entries".format(self.TAG, len(self.entries))
		for i, x in enumerate(self.entries):
			print "  - {:<3}  {:016X} {:016X} {:4} {}".format(i, x[0], x[1], x[2], x[3])
		print ""

#

class xD3E83200_Section(dat1lib.types.sections.Section):
	TAG = 0xD3E83200
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 176..212264 (avg = 5811.9)
		#
		# examples: 82B8360A1DEAFDFD (min size), A8A79439EA51466A (max size)
		
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
		return "D3E83200 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | D3E83200     | {:6} entries".format(self.TAG, len(self.entries))
		if False:
			for i, x in enumerate(self.entries):
				print "  - {:<3}  {:08X} {}".format(i, x, x)
			print ""

#

class xA7D217DE_Section(dat1lib.types.sections.Section):
	TAG = 0xA7D217DE
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 269 occurrences in 724 files
		# size = 1728..1468768 (avg = 66856.1)
		#
		# examples: B851E3356CC7F0B4 (min size), 848B35DDF0C461B6 (max size)
		
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
		return "A7D217DE ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | A7D217DE     | {:6} entries".format(self.TAG, len(self.entries))
		if False:
			for i, x in enumerate(self.entries):
				if i > 100:
					break
				print "  - {:<3}  {:08X} {}".format(i, x, x)
			print ""

#

class xF2A2B07B_Section(dat1lib.types.sections.Section):
	TAG = 0xF2A2B07B
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 368..129032 (avg = 6229.3)
		#
		# examples: 8D46E415B4F7FECA (min size), A8A79439EA51466A (max size)

		# 0x34E97238 contains offsets to something in this section (of different size, ~168 bytes per entry)
		
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
		return "F2A2B07B ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | F2A2B07B     | {:6} entries".format(self.TAG, len(self.entries))
		if False:
			for i, x in enumerate(self.entries):
				print "  - {:<3}  {:08X} {}".format(i, x, x)
			print ""

#

class xF59A5B54_Section(dat1lib.types.sections.Section):
	TAG = 0xF59A5B54
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 48..3752 (avg = 332.8)
		#
		# examples: 8079C2A3952F3D9F (min size), A8A79439EA51466A (max size)
		
		ENTRY_SIZE = 4*14
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<QIIIIIfIIIhHII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

		# same Q as in 0x0A231B40, also the same amount of entries

	def get_short_suffix(self):
		return "F59A5B54 ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | F59A5B54     | {:6} entries".format(self.TAG, len(self.entries))
		for i, x in enumerate(self.entries):
			print "  - {:<3}  {:016X} {:08X} {:3} {:3} {:3} {:3} {:6.3} {:08X} {:08X} {:3} {:6} {:6} {:08X} {:08X}".format(i, *x)
		print ""

#

class xEA8685CD_Section(dat1lib.types.sections.Section):
	TAG = 0xEA8685CD
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 12 occurrences in 724 files
		# size = 1760..42800 (avg = 17277.3)
		#
		# examples: BE93759F2C188519 (min size), BD43160F638170BF (max size)
		
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
		return "EA8685CD ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | EA8685CD     | {:6} entries".format(self.TAG, len(self.entries))

