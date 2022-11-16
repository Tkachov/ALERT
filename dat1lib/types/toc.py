import dat1lib.crc64 as crc64
import dat1lib.types.dat1
import dat1lib.types.sections.toc.archives
import dat1lib.types.sections.toc.asset_ids
import dat1lib.types.sections.toc.offsets
import dat1lib.types.sections.toc.sizes
import dat1lib.types.sections.toc.spans
import io
import os.path
import struct
import zlib

class AssetEntry(object):
	def __init__(self, index, aid, archive, offset, size):
		self.index = index
		self.asset_id = aid
		self.archive = archive
		self.offset = offset
		self.size = size

class TOC(object):
	MAGIC = 0x77AF12AF

	def __init__(self, f):
		self.magic, self.size = struct.unpack("<II", f.read(8))

		if self.magic != self.MAGIC:
			print("[!] Bad 'toc' magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))
		
		dec = zlib.decompressobj(0)
		data = dec.decompress(f.read())

		if len(data) != self.size:
			print("[!] Actual decompressed size {} isn't equal to one written in the file {}".format(len(data), self.size))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(data), self)

		self._archives = {} # (f:FileHandle, compressed:bool)
		self._archives_dir = None

	def save(self, f):
		of = io.BytesIO(bytes())
		self.dat1.save(of)
		of.seek(0)
		uncompressed = of.read()

		c = zlib.compressobj()
		compressed = c.compress(uncompressed)
		compressed += c.flush()
		
		f.write(struct.pack("<II", self.magic, len(uncompressed)))
		f.write(compressed)

	def print_info(self, config):
		print("-------")
		print("TOC {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("-------")
		print("")

		self.dat1.print_info(config)

	#

	def set_archives_dir(self, path):
		for k in self._archives:
			f, _ = self._archives[k]
			f.close()

		self._archives_dir = path
		self._archives = {}

	def _get_archive(self, index):
		if index in self._archives:
			return self._archives[index]

		if self._archives_dir is None:
			print("[!] Can't open archive when 'asset_archive' is not specified")
			return (None, False)

		s = self.get_archives_section()
		fn = s.archives[index].filename

		i = fn.index(b'\0')
		if i != -1:
			fn = fn[:i]
		fn = fn.decode('ascii')
		fn = fn.replace("\\", "/")

		f = open(os.path.join(self._archives_dir, fn), "rb")
		v = struct.unpack("<I", f.read(4))[0]
		compressed = (v == 0x52415344)
		self._archives[index] = (f, compressed)
		return self._archives[index]

	#

	def get_archives_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.archives.ArchivesSection.TAG)

	def get_assets_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.asset_ids.AssetIdsSection.TAG)

	def get_sizes_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.sizes.SizesSection.TAG)

	def get_spans_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.spans.SpansSection.TAG)

	def get_offsets_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.offsets.OffsetsSection.TAG)

	#

	def get_asset_entries_by_path(self, path, stop_on_first=False):
		return self.get_asset_entries_by_assetid(crc64.hash(path), stop_on_first)

	def get_asset_entries_by_assetid(self, aid, stop_on_first=False):
		results = []

		asset_ids = self.get_assets_section().ids
		for i in range(len(asset_ids)): # linear search =\
			if asset_ids[i] == aid:
				results += [self.get_asset_entry_by_index(i)]
				if stop_on_first:
					break

		return results

	def get_asset_entry_by_index(self, index):
		try:
			aid = self.get_assets_section().ids[index]
			off = self.get_offsets_section().entries[index]
			size = self.get_sizes_section().entries[index]
			return AssetEntry(index, aid, off.archive_index, off.offset, size.value)
		except:
			return None

	def extract_asset(self, index_or_entry):
		entry = index_or_entry
		if not isinstance(index_or_entry, AssetEntry):
			entry = self.get_asset_entry_by_index(index_or_entry)

		f, compressed = self._get_archive(entry.archive)
		if not compressed:
			f.seek(entry.offset)
			return f.read(entry.size)

		# TODO: read blocks map once per archive and reuse it
		f.seek(12)
		blocks_header_end = struct.unpack("<I", f.read(4))[0]
		f.seek(32)
		blocks = []
		while f.tell() < blocks_header_end:
			real_offset, _, comp_offset, _, real_size, comp_size, _, _ = struct.unpack("<IIIIIIII", f.read(32))
			blocks += [(real_offset, comp_offset, real_size, comp_size)]

		asset_offset = entry.offset
		asset_end = asset_offset + entry.size

		data = bytearray()

		# TODO: binary search starting block index and ending block index
		# (because this code anyways assumes blocks are sorted by real_offset asc)

		started_reading = False
		for block in blocks:
			real_offset, comp_offset, real_size, comp_size = block

			real_end = real_offset + real_size
			is_first_block = real_offset <= asset_offset and asset_offset < real_end
			is_last_block = real_offset < asset_end and asset_end <= real_end

			if is_first_block:
				started_reading = True

			if started_reading:
				f.seek(comp_offset)
				compressed_data = f.read(comp_size)
				decompressed_data = self._decompress(compressed_data, real_size)
				block_start = max(real_offset, asset_offset) - real_offset
				block_end   = min(asset_end, real_end) - real_offset
				data += decompressed_data[block_start:block_end]

			if is_last_block:
				break

		return data

	def _decompress(self, comp_data, real_size):
		comp_size = len(comp_data)
		real_data = [b'\0' for i in range(real_size)]
		real_i = 0
		comp_i = 0

		while real_i <= real_size and comp_i < comp_size:
			# direct

			a, b = comp_data[comp_i], 0
			comp_i += 1

			if (a & 240) == 240:
				b = comp_data[comp_i]
				comp_i += 1

			direct = (a >> 4) + b
			while direct >= 270 and (direct - 15) % 255 == 0:
				v = comp_data[comp_i]
				comp_i += 1
				direct += v
				if v == 0:
					break

			for i in range(direct):
				if real_i + i >= real_size or comp_i + i >= comp_size:
					break
				real_data[real_i + i] = comp_data[comp_i + i]
			real_i += direct
			comp_i += direct

			reverse = (a & 15) + 4

			if not (real_i <= real_size and comp_i < comp_size):
				break

			# reverse

			a, b = comp_data[comp_i], comp_data[comp_i + 1]
			comp_i += 2

			reverse_offset = a + (b << 8)
			if reverse == 19:
				reverse += comp_data[comp_i]
				comp_i += 1

				while reverse >= 274 and (reverse - 19) % 255 == 0:
					v = comp_data[comp_i]
					comp_i += 1
					reverse += v
					if v == 0:
						break

			for i in range(reverse):
				try:
					real_data[real_i + i] = real_data[real_i - reverse_offset + i]
				except:
					pass
			real_i += reverse

		return bytearray(real_data)
