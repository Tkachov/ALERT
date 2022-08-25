import struct
import math
import string
import os
import os.path
import json
import io
import zlib
import sys
import shutil
import hashlib
import dat1lib

MAGIC = 0x30444F4D # "MOD0"

def calculate_hash(f):
	BUF_SIZE = 65536
	sha1 = hashlib.sha1()

	f.seek(0)
	while True:
		data = f.read(BUF_SIZE)
		if not data:
			break
		sha1.update(data)

	return sha1.hexdigest()

def pretty_info(info):
	try:
		if info["mod_format_version"] == 1:
			return "{} v. {}".format(info["name"], info["mod_version"])

		# try working with unsupported version
		name = info.get("name", None)
		version = info.get("mod_version", None)

		if name is not None:
			result = "{}".format(name)
			if version is not None:
				result += " v. {}".format(version)

		return result
	except:
		pass
	
	return "<unsupported or corrupted mod>"

def get_mods_list(info):
	try:
		if info["format_version"] == 1:
			return info["mods_list"]

		# try working with unsupported version
		return info["mods_list"]
	except:
		pass
	
	return []

def read_toc(fn):
	try:
		f = open(fn, "rb")
		magic, size = struct.unpack("<II", f.read(8))
		dec = zlib.decompressobj(0)
		data = dec.decompress(f.read())
		f.close()

		if magic != 0x77AF12AF:
			print "[!] non-toc magic: {:8X}".format(magic)
			return (False, None)

		f = io.BytesIO(data)
		if len(data) != size:
			print "[!] Actual decompressed size {} isn't equal to one written in the file {}".format(len(data), size)
			return (False, None)

		dat1 = dat1lib.DAT1(f, 0)
		f.close()

		return (True, dat1)
	except Exception as e:
		print "[!] Exception:", e
		return (False, None)

	print "[!] Unknown error occurred while reading 'toc'"
	return (False, None)

def new_archive(toc, fn):
	s = toc.get_section(dat1lib.SECTION_ARCHIVES_MAP)
	new_archive_index = 0
	for a in s.archives:
		if a.install_bucket != 0:
			break
		new_archive_index += 1

	s.archives = s.archives[:new_archive_index] + [dat1lib.ArchiveFileEntry.make(0, 10000 + new_archive_index, fn)] + s.archives[new_archive_index:]
	toc.refresh_section_data(dat1lib.SECTION_ARCHIVES_MAP)

	return new_archive_index

def apply_mod_patch(toc, mod_info, archive_index):
	try:
		assets = toc.get_section(dat1lib.SECTION_ASSET_IDS)
		sizes = toc.get_section(dat1lib.SECTION_SIZE_ENTRIES)
		offsets = toc.get_section(dat1lib.SECTION_OFFSET_ENTRIES)

		def find_asset_index(needle): # linear search =\
			for i, aid in enumerate(assets.ids):
				if aid == needle:
					return i
			return -1

		if mod_info["mod_format_version"] == 1:
			patch = mod_info["patch"]
			for instruction in patch:
				cmd = instruction[0]

				if cmd == "R": # replace
					_, asset_id, archive_offset, asset_size = instruction
					asset_index = find_asset_index(asset_id)
					if asset_index == -1:
						print "[!] Asset {:X} not found".format(asset_id)
						return False

					print sizes.entries[asset_index].value, '=>', asset_size
					print offsets.entries[asset_index].archive_index, '=>', archive_index
					print offsets.entries[asset_index].offset, '=>', archive_offset

					sizes.entries[asset_index].value = asset_size
					offsets.entries[asset_index].archive_index = archive_index
					offsets.entries[asset_index].offset = archive_offset

			toc.refresh_section_data(dat1lib.SECTION_SIZE_ENTRIES)
			toc.refresh_section_data(dat1lib.SECTION_OFFSET_ENTRIES)

			return True
	except:
		pass

	return False

def save_toc(toc, fn):
	of = io.BytesIO(bytes())
	toc.save(of)
	of.seek(0)
	uncompressed = of.read()

	c = zlib.compressobj()
	compressed = c.compress(uncompressed)
	compressed += c.flush()

	f = open(fn, "wb")
	f.write(struct.pack("<II", 0x77AF12AF, len(uncompressed)))
	f.write(compressed)
	f.close()

def main():
	asset_archive_dir = sys.argv[1]
	model_filename = sys.argv[2]

	toc_orig_fn = os.path.join(asset_archive_dir, "toc.orig")
	toc_fn = os.path.join(asset_archive_dir, "toc")
	if not os.path.exists(toc_orig_fn):
		shutil.copyfile(toc_fn, toc_orig_fn)
	
	success, toc = read_toc(toc_orig_fn)
	if not success:
		print "error1"
		return

	#

	f = open(model_filename, "rb")
	data = f.read()
	f.close()

	fn = "hero.mod"
	full_fn = os.path.join(asset_archive_dir, fn)
	f = open(full_fn, "wb")
	f.write(data)
	f.close()

	#

	info = {
		"mod_format_version": 1,
		"mod_version": "1.0.0",
		"author": "Tkachov",
		"name": "Repacked Model",
		"description": "",
		"patch": [
			["R", 9767039763554194594, 0, len(data)]
		]
	}

	index = new_archive(toc, fn)
	if not apply_mod_patch(toc, info, index):
		print "error"
	save_toc(toc, toc_fn)

main()
