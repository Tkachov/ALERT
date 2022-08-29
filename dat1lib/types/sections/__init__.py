import struct

KNOWN_SECTIONS = {}

class Section(object):
	TAG = 0x0
	TYPE = 'unknown'

	def __init__(self, data, container):
		self._raw = data
		self._dat1 = container

	def save(self):
		return self._raw

###

class UintUintMapSection(Section):
	def __init__(self, data, container):
		Section.__init__(self, data, container)

		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self._entries = [struct.unpack("<II", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in xrange(count)]

		self._map = {}
		for (k, v) in self._entries:
			if k in self._map:
				print "[!] Map duplicated key: {:08X}={:08X} replaced with {:08X}={:08X}".format(k, self._map[k], k, v)

			self._map[k] = v

###

class StringsSection(Section):
	def __init__(self, data, container):
		Section.__init__(self, data, container)

		self._strings = data.decode("utf-8").split('\x00')
