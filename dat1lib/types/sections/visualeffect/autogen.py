import dat1lib.types.sections
import io
import struct

#

class x3F03BE86_Section(dat1lib.types.sections.Section):
	TAG = 0x3F03BE86
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 4957 occurrences in 4957 files (always present)
		# size = 120..3600 (avg = 429.4)
		# always first
		#
		# examples: 800DE9729B39D2C0 (min size), 8861893C5DCB68E1 (max size)

		# MM
		# 4215 occurrences in 4215 files (always present)
		# size = 120..5640 (avg = 496.7)
		# always first
		#
		# examples: 800D980A542C48FF (min size), B7543E77981946D6 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "3F03BE86 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 3F03BE86     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x4A868898_Section(dat1lib.types.sections.Section):
	TAG = 0x4A868898
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: none

		# MM
		# 39 occurrences in 4215 files
		# size = 262144..524288 (avg = 289030.5)
		#
		# examples: 85570C67E0242FC3 (min size), 963E914489B953EF (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "4A868898 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 4A868898     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x73CE6A3F_Section(dat1lib.types.sections.Section):
	TAG = 0x73CE6A3F
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 4957 occurrences in 4957 files (always present)
		# size = 32..96 (avg = 32.0)
		#
		# examples: 80047616AB1095BC (min size), 951C0C3671F963AB (max size)

		# MM
		# 4215 occurrences in 4215 files (always present)
		# size = 32..2048 (avg = 99.7)
		#
		# examples: 800B5434AB4FB650 (min size), B61C032770EFB8D4 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "73CE6A3F ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 73CE6A3F     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xAF650E9E_Section(dat1lib.types.sections.Section):
	TAG = 0xAF650E9E
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 4335 occurrences in 4957 files
		# size = 8..184 (avg = 29.7)
		#
		# examples: 800759B19934AEFA (min size), B197FCC9AA19591D (max size)

		# MM
		# 3782 occurrences in 4215 files
		# size = 8..184 (avg = 30.5)
		#
		# examples: 80125190CA9003B4 (min size), 87A5B9E1CE122032 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "AF650E9E ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | AF650E9E     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xB1F4C248_Section(dat1lib.types.sections.Section):
	TAG = 0xB1F4C248
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 4957 occurrences in 4957 files (always present)
		# size = 32..9104 (avg = 1401.5)
		#
		# examples: 807C65DB74F19326 (min size), 8861893C5DCB68E1 (max size)

		# MM
		# 4215 occurrences in 4215 files (always present)
		# size = 32..9504 (avg = 1458.9)
		#
		# examples: 807C65DB74F19326 (min size), A8C73D1D6BA58193 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "B1F4C248 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | B1F4C248     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xB40E134B_Section(dat1lib.types.sections.Section):
	TAG = 0xB40E134B
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 2282 occurrences in 4957 files
		# size = 12..336 (avg = 26.9)
		#
		# examples: 8017ADE1BDFE2140 (min size), A07DC11F8252A8E9 (max size)

		# MM
		# 1940 occurrences in 4215 files
		# size = 12..240 (avg = 24.2)
		#
		# examples: 800D980A542C48FF (min size), 8E715CD9A7856B1F (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "B40E134B ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | B40E134B     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xB86CF442_Section(dat1lib.types.sections.Section):
	TAG = 0xB86CF442
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 4884 occurrences in 4957 files
		# size = 448..16128 (avg = 2253.1)
		#
		# examples: 8009CB09F74A0913 (min size), A3F60265D7731626 (max size)

		# MM
		# 4166 occurrences in 4215 files
		# size = 448..17472 (avg = 2282.2)
		#
		# examples: 800D980A542C48FF (min size), A8C73D1D6BA58193 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "B86CF442 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | B86CF442     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xC3CC2AB5_Section(dat1lib.types.sections.Section):
	TAG = 0xC3CC2AB5
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 3727 occurrences in 4957 files
		# size = 448..12992 (avg = 1803.2)
		#
		# examples: 8009CB09F74A0913 (min size), 8861893C5DCB68E1 (max size)

		# MM
		# 3171 occurrences in 4215 files
		# size = 448..10304 (avg = 1745.5)
		#
		# examples: 80125190CA9003B4 (min size), B617614B7A452EE4 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "C3CC2AB5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | C3CC2AB5     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xD78E007C_Section(dat1lib.types.sections.Section):
	TAG = 0xD78E007C
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 4957 occurrences in 4957 files (always present)
		# size = 32..8096 (avg = 1118.9)
		#
		# examples: 807C65DB74F19326 (min size), 8861893C5DCB68E1 (max size)

		# MM
		# 4215 occurrences in 4215 files (always present)
		# size = 32..7888 (avg = 1149.0)
		#
		# examples: 807C65DB74F19326 (min size), A8C73D1D6BA58193 (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "D78E007C ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | D78E007C     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xEFD8600D_Section(dat1lib.types.sections.Section):
	TAG = 0xEFD8600D
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR
		# 47 occurrences in 4957 files
		# size = 16
		#
		# examples: 80FBDF3F60EA9D9C

		# MM
		# 30 occurrences in 4215 files
		# size = 16
		#
		# examples: 80FBDF3F60EA9D9C
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "EFD8600D ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | EFD8600D     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xECC0D7AF_Section(dat1lib.types.sections.Section):
	TAG = 0xECC0D7AF
	TYPE = 'VisualEffect'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: none

		# MM
		# 39 occurrences in 4215 files
		# size = 24..48 (avg = 26.4)
		#
		# examples: 85570C67E0242FC3 (min size), 963E914489B953EF (max size)
		
		ENTRY_SIZE = 4
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<I", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<I", e))
		of.seek(0)
		return of.read()

	def get_short_suffix(self):
		return "ECC0D7AF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | ECC0D7AF     | {:6} entries".format(self.TAG, len(self.entries)))
