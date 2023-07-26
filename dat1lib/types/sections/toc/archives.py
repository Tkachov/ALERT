import dat1lib.types.sections
import io
import struct

class ArchiveFileEntry(object):
	def __init__(self, data, version):
		self._version = version

		if version == dat1lib.VERSION_RCRA:
			self.filename = data[:40] # acutally contains some stuff after '\0'
			self.a, self.b, self.c, self.d, self.e = struct.unpack("<QQIHI", data[40:])
			# typically 2678794514496 2678794514496 3844228203 32763 0
			# sometimes e is different
		else:
			self.filename = data[8:]
			self.install_bucket, self.chunkmap = struct.unpack("<II", data[:8])

	@classmethod
	def make(cls, bucket, chunk, filename):
		data = struct.pack("<II", bucket, chunk)
		f = io.BytesIO()
		f.write(data)
		f.write(filename.encode('ascii'))
		LN = 64
		if self._version == dat1lib.VERSION_SO:
			LN = 16
		if len(filename) < LN:
			f.write(b'\0' * (LN - len(filename)))
		f.seek(0)
		return cls(f.read())

class ArchivesSection(dat1lib.types.sections.Section):
	TAG = 0x398ABFF0
	TYPE = 'toc'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		self.version = self._dat1.version
		if self.version is None:
			if len(data) % 66 == 0:
				self.version = dat1lib.VERSION_RCRA
			elif len(data) % 72 == 0:
				self.version = dat1lib.VERSION_MSMR
			elif len(data) % 24 == 0:
				self.version = dat1lib.VERSION_SO

		ENTRY_SIZE = 72
		if self.version == dat1lib.VERSION_SO:
			ENTRY_SIZE = 24
		elif self.version == dat1lib.VERSION_RCRA:
			ENTRY_SIZE = 66

		count = len(data)//ENTRY_SIZE
		self.archives = [ArchiveFileEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE], self.version) for i in range(count)]

	def save(self):
		of = io.BytesIO(bytes())
		for e in self.archives:
			of.write(struct.pack("<II", e.install_bucket, e.chunkmap))
			of.write(e.filename)
		of.seek(0)
		return bytearray(of.read())

	def get_short_suffix(self):
		return "archives ({})".format(len(self.archives))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Archives Map | {:6} entries".format(self.TAG, len(self.archives)))
