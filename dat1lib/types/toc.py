# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib
import dat1lib.crc64 as crc64
import dat1lib.decompression as decompression
import dat1lib.gdeflate as gdeflate
import dat1lib.types.sections.toc.asset
import dat1lib.types.sections.toc.file
import dat1lib.types.sections.toc.header
import dat1lib.types.sections.toc.texture
import io
import os.path
import struct
import zlib

class AssetEntry(object):
	def __init__(self, index, aid, metadata, header):
		self.index = index
		self.asset_id = aid
		self.metadata = metadata
		self.header = header

	def size(self):
		return self.metadata.size

	def offset(self):
		return self.metadata.offset

	def archive(self):
		return self.metadata.archive_index

class TOC(object):
	MAGIC = 0x34E89035

	def __init__(self, f):
		self.magic, self.size = struct.unpack("<II", f.read(8))

		if self.magic != self.MAGIC:
			print(f"[!] Bad 'toc' magic: {self.magic:08X} (isn't equal to expected {self.MAGIC:08X})")
		
		data = f.read()

		if len(data) < self.size:
			print(f"[!] Less data ({len(data)} bytes) than was promised in the file ({self.size} bytes)")

		self.dat1 = dat1lib.read_dat1(io.BytesIO(data))

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
		fn = s.archives[index].get_filename()
		fn = fn.replace("\\", "/")

		f = open(os.path.join(self._archives_dir, fn), "rb")
		v = struct.unpack("<I", f.read(4))[0]
		compressed = (v == 0x52415344)
		self._archives[index] = (f, compressed)

		return self._archives[index]

	#

	def get_header_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.header.HeaderSection.TAG)

	def get_file_metadata_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.file.FileMetadataSection.TAG)

	def get_asset_ids_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.asset.AssetIdsSection.TAG)

	def get_asset_metadata_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.asset.AssetMetadataSection.TAG)

	def get_asset_header_data_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.asset.AssetHeaderDataSection.TAG)

	def get_texture_header_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.texture.TextureHeaderSection.TAG)

	def get_texture_asset_ids_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.texture.TextureAssetIdsSection.TAG)

	def get_texture_meta_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.texture.TextureMetaSection.TAG)

	# old aliases

	def get_archives_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.file.FileMetadataSection.TAG)

	def get_assets_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.asset.AssetIdsSection.TAG)

	def get_spans_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.header.HeaderSection.TAG)

	def get_asset_headers_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.asset.AssetHeaderDataSection.TAG)

	def get_textures_section(self):
		return self.dat1.get_section(dat1lib.types.sections.toc.texture.TextureAssetIdsSection.TAG)

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
			assets_section = self.get_assets_section()
			asset_metadata_section = self.get_asset_metadata_section()

			aid = assets_section.ids[index]
			metadata = asset_metadata_section.entries[index]

			header = None
			if metadata.header_offset != -1:
				headers_section = self.get_asset_headers_section()
				header = headers_section.read_header(metadata.header_offset)

			return AssetEntry(index, aid, metadata, header)
		except:
			return None

	def extract_asset(self, index_or_entry):
		entry = index_or_entry
		if not isinstance(index_or_entry, AssetEntry):
			entry = self.get_asset_entry_by_index(index_or_entry)

		f, compressed = self._get_archive(entry.archive())
		if not compressed:
			f.seek(entry.offset())
			return f.read(entry.size())

		# TODO: read blocks map once per archive and reuse it
		f.seek(12)
		blocks_header_end = struct.unpack("<I", f.read(4))[0]
		f.seek(32)
		blocks = []
		while f.tell() < blocks_header_end:
			real_offset, _, comp_offset, _, real_size, comp_size, comp_type, _, _, _ = struct.unpack("<IIIIIIBBHI", f.read(32))
			blocks += [(real_offset, comp_offset, real_size, comp_size, comp_type)]

		asset_offset = entry.offset()
		asset_end = asset_offset + entry.size()

		data = bytearray()

		# TODO: binary search starting block index and ending block index
		# (because this code anyways assumes blocks are sorted by real_offset asc)

		started_reading = False
		for block in blocks:
			real_offset, comp_offset, real_size, comp_size, comp_type = block

			real_end = real_offset + real_size
			is_first_block = real_offset <= asset_offset and asset_offset < real_end
			is_last_block = real_offset < asset_end and asset_end <= real_end

			if is_first_block:
				started_reading = True

			if started_reading:
				f.seek(comp_offset)
				compressed_data = f.read(comp_size)

				decompressed_data = None
				if comp_type == 2:
					decompressed_data = gdeflate.decompress(compressed_data, real_size)				
				elif comp_type == 3:
					decompressed_data = decompression.decompress(compressed_data, real_size)
				else:
					decompressed_data = bytearray(real_size)

				block_start = max(real_offset, asset_offset) - real_offset
				block_end   = min(asset_end, real_end) - real_offset
				data += decompressed_data[block_start:block_end]

			if is_last_block:
				break

		return data
