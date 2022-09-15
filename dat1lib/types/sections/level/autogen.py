import dat1lib.types.sections
import io
import struct

#

class x07C75341_Section(dat1lib.types.sections.Section):
	TAG = 0x07C75341
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 15008184
		#
		# examples: 93243FC0D3FE0498
		
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
		return "07C75341 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 07C75341     | {:6} entries".format(self.TAG, len(self.entries))

#

class x2236C47A_Section(dat1lib.types.sections.Section):
	TAG = 0x2236C47A
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 8920
		#
		# examples: 93243FC0D3FE0498
		
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
		return "2236C47A ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2236C47A     | {:6} entries".format(self.TAG, len(self.entries))

#

class x2BA33702_Section(dat1lib.types.sections.Section):
	TAG = 0x2BA33702
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 49212
		#
		# examples: 93243FC0D3FE0498
		
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
		return "2BA33702 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 2BA33702     | {:6} entries".format(self.TAG, len(self.entries))

#

class x3395AEC1_Section(dat1lib.types.sections.Section):
	TAG = 0x3395AEC1
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 107040
		#
		# examples: 93243FC0D3FE0498
		
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
		return "3395AEC1 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 3395AEC1     | {:6} entries".format(self.TAG, len(self.entries))

#

class x339C970E_Section(dat1lib.types.sections.Section):
	TAG = 0x339C970E
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 996932
		#
		# examples: 93243FC0D3FE0498
		
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
		return "339C970E ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 339C970E     | {:6} entries".format(self.TAG, len(self.entries))

#

class x396F9418_Section(dat1lib.types.sections.Section):
	TAG = 0x396F9418
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 66348
		#
		# examples: 93243FC0D3FE0498
		
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
		return "396F9418 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 396F9418     | {:6} entries".format(self.TAG, len(self.entries))

#

class x4130D903_Section(dat1lib.types.sections.Section):
	TAG = 0x4130D903
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 7372
		#
		# examples: 93243FC0D3FE0498
		
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
		return "4130D903 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 4130D903     | {:6} entries".format(self.TAG, len(self.entries))

#

class x41887FB3_Section(dat1lib.types.sections.Section):
	TAG = 0x41887FB3
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 12560
		#
		# examples: 93243FC0D3FE0498
		
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
		return "41887FB3 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 41887FB3     | {:6} entries".format(self.TAG, len(self.entries))

#

class x4E023760_Section(dat1lib.types.sections.Section):
	TAG = 0x4E023760
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 147636
		#
		# examples: 93243FC0D3FE0498
		
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
		return "4E023760 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 4E023760     | {:6} entries".format(self.TAG, len(self.entries))

#

class x611F490D_Section(dat1lib.types.sections.Section):
	TAG = 0x611F490D
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 9680
		# always last
		#
		# examples: 93243FC0D3FE0498
		
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
		return "611F490D ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 611F490D     | {:6} entries".format(self.TAG, len(self.entries))

#

class x6251A0BF_Section(dat1lib.types.sections.Section):
	TAG = 0x6251A0BF
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 132
		#
		# examples: 93243FC0D3FE0498
		
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
		return "6251A0BF ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 6251A0BF     | {:6} entries".format(self.TAG, len(self.entries))

#

class x7077E5F5_Section(dat1lib.types.sections.Section):
	TAG = 0x7077E5F5
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 2244
		#
		# examples: 93243FC0D3FE0498
		
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
		return "7077E5F5 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 7077E5F5     | {:6} entries".format(self.TAG, len(self.entries))

#

class x7CA7267D_Section(dat1lib.types.sections.Section):
	TAG = 0x7CA7267D
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 36
		# always first
		#
		# examples: 93243FC0D3FE0498
		
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
		return "7CA7267D ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 7CA7267D     | {:6} entries".format(self.TAG, len(self.entries))

#

class x95F91E24_Section(dat1lib.types.sections.Section):
	TAG = 0x95F91E24
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 41632
		#
		# examples: 93243FC0D3FE0498
		
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
		return "95F91E24 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | 95F91E24     | {:6} entries".format(self.TAG, len(self.entries))

#

class xC30D92B6_Section(dat1lib.types.sections.Section):
	TAG = 0xC30D92B6
	TYPE = 'Level'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# size = 17712
		#
		# examples: 93243FC0D3FE0498
		
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
		return "C30D92B6 ({})".format(len(self.entries))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | C30D92B6     | {:6} entries".format(self.TAG, len(self.entries))

