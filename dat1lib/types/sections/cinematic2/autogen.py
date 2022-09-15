import dat1lib.types.sections
import io
import struct

#

class x0A231B40_Section(dat1lib.types.sections.Section):
	TAG = 0x0A231B40
	TYPE = 'Cinematic2'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 724 occurrences in 724 files (always present)
		# size = 16..1072 (avg = 95.9)
		#
		# examples: 8003278FC28C9C4B (min size), A8A79439EA51466A (max size)
		
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
		return "0A231B40 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 0A231B40     | {:6} entries".format(self.TAG, len(self.entries))

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
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in xrange(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "0CDE73EF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 0CDE73EF     | {:6} entries".format(self.TAG, len(self.entries))

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
		return "13AAEFE2 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 13AAEFE2     | {:6} entries".format(self.TAG, len(self.entries))

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
		pass

	def get_short_suffix(self):
		return "15C2983A ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 15C2983A     | {:6} bytes".format(self.TAG, len(self._raw))

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
		return "2029471C ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2029471C     | {:6} entries".format(self.TAG, len(self.entries))

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
		return "26AB8388 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 26AB8388     | {:6} entries".format(self.TAG, len(self.entries))

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
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2D9B0A30     | {:6} bytes".format(self.TAG, len(self._raw))

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
		return "2F161636 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2F161636     | {:6} entries".format(self.TAG, len(self.entries))

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
		pass

	def get_short_suffix(self):
		return "2EF690BD ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2EF690BD     | {:6} bytes".format(self.TAG, len(self._raw))

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
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 34E97238     | {:6} entries".format(self.TAG, len(self.entries))

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
		return "5BE2A972 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 5BE2A972     | {:6} entries".format(self.TAG, len(self.entries))

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
		pass

	def get_short_suffix(self):
		return "85272DB0 ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 85272DB0     | {:6} bytes".format(self.TAG, len(self._raw))

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
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 7EF72163     | {:6} entries".format(self.TAG, len(self.entries))

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
		return "802A0575 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 802A0575     | {:6} entries".format(self.TAG, len(self.entries))

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
		return "A20AD331 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | A20AD331     | {:6} entries".format(self.TAG, len(self.entries))

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
		return "ADCF5096 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | ADCF5096     | {:6} entries".format(self.TAG, len(self.entries))

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
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | D3E83200     | {:6} entries".format(self.TAG, len(self.entries))

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
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | A7D217DE     | {:6} entries".format(self.TAG, len(self.entries))

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
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | F2A2B07B     | {:6} entries".format(self.TAG, len(self.entries))

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
		return "F59A5B54 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | F59A5B54     | {:6} entries".format(self.TAG, len(self.entries))

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
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | EA8685CD     | {:6} entries".format(self.TAG, len(self.entries))

