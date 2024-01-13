import dat1lib.types.sections
import io
import struct

class AssetHeadersSection(dat1lib.types.sections.Section):
	TAG = 0x654BDED9 # Archive TOC Asset Header Data
	TYPE = 'toc'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 36
		count = len(data)//ENTRY_SIZE
		self.headers = [data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.headers:
			of.write(e)
		of.seek(0)
		return bytearray(of.read())

	def get_short_suffix(self):
		return "headers ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Asset Hdrs   | {:6} entries".format(self.TAG, len(self.entries)))

class TexturesSection(dat1lib.types.sections.Section):
	TAG = 0x36A6C8CC # Archive TOC Texture Asset Ids
	TYPE = 'toc'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.ids = [struct.unpack("<Q", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE])[0] for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for aid in self.ids:
			of.write(struct.pack("<Q", aid))
		of.seek(0)
		return bytearray(of.read())

	def get_short_suffix(self):
		return "textures ({})".format(len(self.ids))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Textures     | {:6} entries".format(self.TAG, len(self.ids)))

		for aid in self.ids:
			print("    - {:016X}".format(aid))

# 0x62297090 # Archive TOC Texture Header # one <I
# 0xC9FB9DDA # Archive TOC Texture Meta   # 72 bytes per texture
