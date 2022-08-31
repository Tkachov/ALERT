import io
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

###

# based off of https://github.com/team-waldo/InsomniacArchive/blob/spiderman_pc/InsomniacArchive/Section/SerializedObjectSection.cs

class SerializedSection(Section):
	NT_UINT8 		= 0x00
	NT_UINT16 		= 0x01
	NT_UINT32 		= 0x02
	NT_INT8 		= 0x04
	NT_INT16 		= 0x05
	NT_INT32 		= 0x06
	NT_FLOAT 		= 0x08
	NT_STRING 		= 0x0A
	NT_OBJECT 		= 0x0D
	NT_BOOLEAN 		= 0x0F
	NT_INSTANCE_ID 	= 0x11 # 8 bytes
	NT_NULL 		= 0x13 # 1 byte, always zero. maybe null?

	def __init__(self, data, container):
		Section.__init__(self, data, container)

		f = io.BytesIO(data)
		self.root = self._deserialize(f)
		self.extras = []
		while f.tell() < len(data):
			self.extras += [self._deserialize(f)]

	def _deserialize(self, f):
		return self._deserialize_object(f)

	def _deserialize_object(self, f):
		result = {}

		zero, unknown, children_count, data_len = struct.unpack("<IIII", f.read(16))
		if zero != 0 or unknown != 0x03150044:
			print "[!] Strange serialized object header: zero={}, unknown={:08X}".format(zero, unknown)

		start = f.tell()
		children = [struct.unpack("<IHBB", f.read(8)) for i in xrange(children_count)]
		# (hash, flags, unknown, node_type)
		children_offsets = [struct.unpack("<I", f.read(4)) for i in xrange(children_count)]

		for i in xrange(children_count):
			name = self._dat1.get_string(children_offsets[i][0])

			items_count = children[i][1] >> 4
			is_array = items_count > 1

			if is_array:
				result[name] = self._deserialize_array(f, children[i][3], items_count)
			else:
				result[name] = self._deserialize_node(f, children[i][3])

		self._align(f, 4)

		finish = f.tell()
		left = data_len - (finish - start)
		if left < 0:
			print "[!] Read more data ({}) than expected ({})".format(finish - start, data_len)
		elif left > 0:
			f.read(left)

		return result

	def _deserialize_array(self, f, item_type, items_count):
		return [self._deserialize_node(f, item_type) for i in xrange(items_count)]

	def _deserialize_node(self, f, item_type):
		if item_type == self.NT_UINT8:
			return struct.unpack("<B", f.read(1))[0]

		if item_type == self.NT_UINT16:
			return struct.unpack("<H", f.read(2))[0]

		if item_type == self.NT_UINT32:
			return struct.unpack("<I", f.read(4))[0]

		if item_type == self.NT_INT8:
			return struct.unpack("<b", f.read(1))[0]

		if item_type == self.NT_INT16:
			return struct.unpack("<h", f.read(2))[0]

		if item_type == self.NT_INT32:
			return struct.unpack("<i", f.read(4))[0]

		if item_type == self.NT_FLOAT:
			return struct.unpack("<f", f.read(4))[0]

		if item_type == self.NT_STRING:
			return self._deserialize_string(f)

		if item_type == self.NT_OBJECT:
			return self._deserialize_object(f)

		if item_type == self.NT_BOOLEAN:
			return (struct.unpack("<B", f.read(1))[0] != 0)

		if item_type == self.NT_INSTANCE_ID:
			return struct.unpack("<Q", f.read(8))[0]

		if item_type == self.NT_NULL:
			f.read(1)
			return None

		print "[!] Unknown node_type={}".format(item_type)
		return None

	def _deserialize_string(self, f):
		length, h32, h64 = struct.unpack("<IIQ", f.read(16))
		v = f.read(length)
		f.read(1) # nullbyte
		self._align(f, 4)
		return v

	def _align(self, f, a):
		r = f.tell() % a
		if r != 0:
			f.read(a - r)
