import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
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
		self._entries = [struct.unpack("<II", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

		self._map = {}
		for (k, v) in self._entries:
			if k in self._map:
				print("[!] Map duplicated key: {:08X}={:08X} replaced with {:08X}={:08X}".format(k, self._map[k], k, v))

			self._map[k] = v

###

class StringsSection(Section):
	def __init__(self, data, container):
		Section.__init__(self, data, container)

		self._strings = data.decode("utf-8").split('\x00')
		if self._strings[-1] == "":
			self._strings.pop()
		self._strings_map = {}

		offset = 0
		for s in self._strings:
			self._strings_map[offset] = s
			offset += len(s) + 1

	def get_string(self, offset):
		print("{} {}".format(offset, self._strings_map))
		return self._strings_map.get(offset, None)

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

	@classmethod
	def make(cls, root, extras, container):
		data = struct.pack("<IIII", 0, 0x03150044, 0, 0) # equivalent of {}
		c = cls(data, container)
		c.root = root
		c.extras = extras
		return c

	def save(self):
		self._serialize_self()
		return self._raw

	#

	def _deserialize(self, f):
		return self._deserialize_object(f)

	def _deserialize_object(self, f):
		result = {}

		zero, unknown, children_count, data_len = struct.unpack("<IIII", f.read(16))
		if zero != 0 or unknown != 0x03150044:
			print("[!] Strange serialized object header: zero={}, unknown={:08X}".format(zero, unknown))

		start = f.tell()
		children = [struct.unpack("<IHBB", f.read(8)) for i in range(children_count)]
		# (hash, flags, unknown, node_type)
		children_offsets = [struct.unpack("<I", f.read(4)) for i in range(children_count)]

		for i in range(children_count):
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
			print("[!] Read more data ({}) than expected ({})".format(finish - start, data_len))
		elif left > 0:
			f.read(left)

		return result

	def _deserialize_array(self, f, item_type, items_count):
		return [self._deserialize_node(f, item_type) for i in range(items_count)]

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

		print("[!] Unknown node_type={}".format(item_type))
		return None

	def _deserialize_string(self, f):
		length, h32, h64 = struct.unpack("<IIQ", f.read(16))
		v = f.read(length)
		f.read(1) # nullbyte
		self._align(f, 4)
		return v.decode('ascii')

	def _align(self, f, a):
		r = f.tell() % a
		if r != 0:
			f.read(a - r)

	#

	def _serialize_self(self):
		f = io.BytesIO(bytes())
		self._serialize(f, self.root)
		for e in self.extras:
			self._serialize(f, e)
		
		f.seek(0)
		self._raw = f.read()

	def _serialize(self, f, obj):
		self._serialize_object(f, obj)

	def _serialize_object(self, f, obj):
		if type(obj) != dict:
			print("[!] Serialization error: object expected, got '{}'".format(type(obj)))
			return

		children = obj.items()
		string_offsets = [self._dat1.add_string(k) for k, v in children]

		f2 = io.BytesIO(bytes())

		def get_int_type(mn, mx):
			RANGES = [
				(self.NT_UINT8, 0, 255),
				(self.NT_UINT16, 0, 65535),
				(self.NT_UINT32, 0, 2**32 - 1),
				(self.NT_INSTANCE_ID, 0, 2**64 - 1),
				
				(self.NT_INT8, -128, 127),
				(self.NT_INT16, -32768, 32767),
				(self.NT_INT32, -(2**31), 2**31 - 1),
				(self.NT_INSTANCE_ID, -(2**63), 2**63 - 1) # technically wrong, but just in case
			]

			for rt, rmn, rmx in RANGES:
				if rmn <= mn and mx <= rmx:
					return rt

			print("[!] Serialization error: provided int (in range {}..{}) can't fit any of supported types".format(mn, mx))
			return self.NT_INSTANCE_ID

		def get_item_type(v):
			if v is None:
				return self.NT_NULL

			t = type(v)
			if t == bool:
				return self.NT_BOOLEAN

			if t == float:
				return self.NT_FLOAT

			if t == str:
				return self.NT_STRING

			if t == dict:
				return self.NT_OBJECT

			if t == list:
				if len(v) == 0:
					print("[!] Serialization error: can't find type of empty list")

				t2 = type(v[0])
				if t2 == int:
					return get_int_type(min(v), max(v))
				return get_item_type(v[0])

			if t == int:
				return get_int_type(v, v)

			print("[!] Serialization error: can't serialize '{}'".format(t))
			return self.NT_NULL

		children_types = [get_item_type(v) for k, v in children]

		for (k, v), t in zip(children, children_types):
			hsh = crc32.hash(k, False)
			flags = 1 << 4			
			if type(v) == list:
				flags = len(v) << 4
			f2.write(struct.pack("<IHBB", hsh, flags, 0, t))

		for so in string_offsets:
			f2.write(struct.pack("<I", so))

		for (k, v), t in zip(children, children_types):
			if type(v) == list:
				self._serialize_array(f2, v, t)
			else:
				self._serialize_node(f2, v, t)

		self._pad(f2, 4)

		f2.seek(0)
		children_data = f2.read()

		f.write(struct.pack("<IIII", 0, 0x03150044, len(children), len(children_data)))
		f.write(children_data)

	def _serialize_array(self, f, arr, item_type):
		for v in arr:
			self._serialize_node(f, v, item_type)

	def _serialize_node(self, f, node, item_type):
		if item_type == self.NT_UINT8:
			f.write(struct.pack("<B", node))
			return

		if item_type == self.NT_UINT16:
			f.write(struct.pack("<H", node))
			return

		if item_type == self.NT_UINT32:
			f.write(struct.pack("<I", node))
			return

		if item_type == self.NT_INT8:
			f.write(struct.pack("<b", node))
			return

		if item_type == self.NT_INT16:
			f.write(struct.pack("<h", node))
			return

		if item_type == self.NT_INT32:
			f.write(struct.pack("<i", node))
			return

		if item_type == self.NT_FLOAT:
			f.write(struct.pack("<f", node))
			return

		if item_type == self.NT_STRING:
			self._serialize_string(f, node)
			return

		if item_type == self.NT_OBJECT:
			self._serialize_object(f, node)
			return

		if item_type == self.NT_BOOLEAN:
			f.write(struct.pack("<B", int(node)))
			return

		if item_type == self.NT_INSTANCE_ID:
			f.write(struct.pack("<Q", node))
			return

		if item_type == self.NT_NULL:
			f.write(b'\0')
			return

		print("[!] Serialization error: unknown node_type={}".format(item_type))
		f.write(b'\0')

	def _serialize_string(self, f, s):
		s = str(s)
		f.write(struct.pack("<IIQ", len(s), crc32.hash(s, False), crc64.hash(s)))
		f.write(s.encode('ascii'))
		f.write(b'\0')
		self._pad(f, 4)

	def _pad(self, f, a):
		r = f.tell() % a
		if r != 0:
			f.write(b'\0' * (a - r))

###

class ReferencesSection(Section):
	def __init__(self, data, container):
		Section.__init__(self, data, container)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.entries = [struct.unpack("<QII", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.entries:
			of.write(struct.pack("<QII", *e))
		of.seek(0)
		return of.read()

	def print_verbose(self, config):
		# crc32s of ".actor", ".config", etc
		EXTENSIONS_HASHES = {
			0x37E72F50: "Actor",
			0xA9C3E1B8: "AnimClip",
			0xD1AD9F7C: "AnimSet",
			0xF56C78E4: "Atmosphere",
			0x57B67E8F: "Cinematic2",
			0xEA7EFDD4: "Conduit",
			0xA9F149C4: "Config",
			0xE978B5BA: "Level",
			0x08BD74BA: "LevelLight",
			0x29E2F18F: "Localization",
			0xB5AAFACC: "Material",
			0x47048393: "MaterialGraph",
			0xA4070B70: "Model",
			0x53B8EA03: "NodeGraph",
			0x9676F576: "PerformanceClip",
			0xD1BF8CDA: "PerformanceSet",
			0xFFA86BB6: "Soundbank",
			0x95A3A227: "Texture",
			0xDABA2AEA: "VisualEffect",
			0xD8A92608: "WwiseLookup",
			0xE1EE9AA6: "Zone"
		}

		for i, x in enumerate(self.entries):
			s = self._dat1.get_string(x[1])
			ext = EXTENSIONS_HASHES.get(x[2], "{:08X}".format(x[2]))
			print("  - {:<2}  {:016X}  {}{} {}".format(i, x[0], ext, (16 - len(ext))*" ", s))
			if config.get("section_warnings", True):
				if s is not None:
					real_hash = crc64.hash(s)
					if real_hash != x[0]:
						print("        [!] filename real hash {:016X} is not equal to one written in the struct {:016X}".format(real_hash, x[0]))
		print("")
