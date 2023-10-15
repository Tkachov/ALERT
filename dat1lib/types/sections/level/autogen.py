import dat1lib.types.sections
import io
import struct

# there's only 1 Level:
# - SO      -- 34ABC921         (levels/sunset_city/sunset_city.level)
# - MSMR/MM -- 93243FC0D3FE0498 (levels/i20_city/i20_city.level)
# - RCRA    -- 95A02E80D5D79CF7 (levels/i29/i29.level)

#

class x07C75341_Section(dat1lib.types.sections.Section):
	TAG = 0x07C75341
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: size = 15008184
		# MM: size = 13217072
		# RCRA: size = 3827392
		
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
		return "07C75341 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 07C75341     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x2236C47A_Section(dat1lib.types.sections.Section):
	TAG = 0x2236C47A
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 11844
		# MSMR: size = 8920
		# MM: size = 8420
		# RCRA: size = 3440
		
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
		return "2236C47A ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 2236C47A     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x2BA33702_Section(dat1lib.types.sections.Section):
	TAG = 0x2BA33702
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 14916
		# MSMR: size = 49212
		# MM: size = 42124
		# RCRA: size = 36704
		
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
		return "2BA33702 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 2BA33702     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x3395AEC1_Section(dat1lib.types.sections.Section):
	TAG = 0x3395AEC1
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 118440
		# MSMR: size = 107040
		# MM: size = 101040
		# RCRA: size = 41280
		
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
		return "3395AEC1 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 3395AEC1     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x339C970E_Section(dat1lib.types.sections.Section):
	TAG = 0x339C970E
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 383992
		# MSMR: size = 996932
		# MM: size = 266284
		# RCRA: size = 148492
		
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
		return "339C970E ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 339C970E     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x396F9418_Section(dat1lib.types.sections.Section):
	TAG = 0x396F9418
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 15712
		# MSMR: size = 66348
		# MM: size = 50724
		# RCRA: size = 43776
		
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
		return "396F9418 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 396F9418     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x4130D903_Section(dat1lib.types.sections.Section):
	TAG = 0x4130D903
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 1964
		# MSMR: size = 7372
		# MM: size = 5636
		# RCRA: size = 4864
		
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
		return "4130D903 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 4130D903     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x41887FB3_Section(dat1lib.types.sections.Section):
	TAG = 0x41887FB3
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 4032
		# MSMR: size = 12560
		# MM: size = 8384
		# RCRA: size = 4992
		
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
		return "41887FB3 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 41887FB3     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x4E023760_Section(dat1lib.types.sections.Section):
	TAG = 0x4E023760
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 29832
		# MSMR: size = 147636
		# MM: size = 126372
		# RCRA: size = 110112
		
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
		return "4E023760 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 4E023760     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x611F490D_Section(dat1lib.types.sections.Section):
	TAG = 0x611F490D
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: size = 9680
		# MM: size = 8760
		# RCRA: size = 4904
		# always last
		
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
		return "611F490D ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 611F490D     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x6251A0BF_Section(dat1lib.types.sections.Section):
	TAG = 0x6251A0BF
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: size = 132
		# MM: size = 128
		# RCRA: none
		
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
		return "6251A0BF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 6251A0BF     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x7077E5F5_Section(dat1lib.types.sections.Section):
	TAG = 0x7077E5F5
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# MSMR: size = 2244
		# MM: size = 1452
		# RCRA: size = 1412
		
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
		return "7077E5F5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 7077E5F5     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x7CA7267D_Section(dat1lib.types.sections.Section):
	TAG = 0x7CA7267D
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 36
		# MSMR: size = 36
		# MM: size = 36
		# RCRA: size = 36
		# always first
		
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
		return "7CA7267D ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 7CA7267D     | {:6} entries".format(self.TAG, len(self.entries)))

#

class x95F91E24_Section(dat1lib.types.sections.Section):
	TAG = 0x95F91E24
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 9702
		# MSMR: size = 41632
		# MM: size = 31346
		# RCRA: size = 20270
		
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
		return "95F91E24 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | 95F91E24     | {:6} entries".format(self.TAG, len(self.entries)))

#

class xC30D92B6_Section(dat1lib.types.sections.Section):
	TAG = 0xC30D92B6
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO: size = 7040
		# MSMR: size = 17712
		# MM: size = 17904
		# RCRA: size = 22032
		
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
		return "C30D92B6 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | C30D92B6     | {:6} entries".format(self.TAG, len(self.entries)))

