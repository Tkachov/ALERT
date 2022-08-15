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

	# print "uncompressed size = {}".format(len(uncompressed))

	c = zlib.compressobj()
	compressed = c.compress(uncompressed)
	compressed += c.flush()

	f = open(fn, "wb")
	f.write(struct.pack("<II", 0x77AF12AF, len(uncompressed)))
	f.write(compressed)
	f.close()

def main():
	asset_archive_dir = sys.argv[1]
	files = os.listdir(asset_archive_dir)

	detected_mods = {}
	for fn in files:
		if not fn.endswith(".mod"):
			continue

		fullname = os.path.join(asset_archive_dir, fn)
		f = open(fullname, "rb")
		f.seek(-8, io.SEEK_END)
		magic, size = struct.unpack("<II", f.read(8))

		if magic != MAGIC:
			continue

		f.seek(-8 - size, io.SEEK_END)
		info = json.loads(f.read(size))
		fhash = calculate_hash(f)
		f.close()

		detected_mods[fn] = (fn, info, fhash)

	if len(detected_mods) == 0:
		print "No mods detected."
	else:
		print "Detected mods:"
		for k in detected_mods:
			fn, info, _ = detected_mods[k]
			print " ", fn, "|", pretty_info(info)
	print ""

	#

	toc_orig_fn = os.path.join(asset_archive_dir, "toc.orig")
	toc_fn = os.path.join(asset_archive_dir, "toc")
	if not os.path.exists(toc_orig_fn):
		shutil.copyfile(toc_fn, toc_orig_fn)

	#

	success, toc = read_toc(toc_fn)
	if not success:
		return

	#

	mod_section = toc.get_section(dat1lib.SECTION_MOD)
	mods_info = {
		"format_version": 1,
		"mods_list": []
	}
	if mod_section is not None:
		mods_info = mod_section.data

	mods_list = get_mods_list(mods_info)

	if len(mods_list) == 0:
		print "No mods installed."
	else:
		print "Installed mods:"
		for m in mods_info["mods_list"]:
			mod_filename, mod_filehash = m
			status = ""

			if mod_filename in detected_mods:
				_, _, fhash = detected_mods[mod_filename]
				if fhash == mod_filehash:
					status = "OK"
				else:
					status = "Different version of a mod installed"
			else:
				status = "Not found"

			print " ", mod_filename, "|", status

	print ""

	#

	# installing all mods just as a PoC
	
	success, toc = read_toc(toc_orig_fn)
	if not success:
		return

	new_mods_info = {
		"format_version": 1,
		"mods_list": []
	}
	for k in detected_mods:
		fn, info, fhash = detected_mods[k]
		print "Installing '{}'...".format(fn)
		index = new_archive(toc, fn)
		apply_mod_patch(toc, info, index)
		new_mods_info["mods_list"] += [[fn, fhash]]

	toc.add_section(dat1lib.SECTION_MOD, json.dumps(new_mods_info))
	save_toc(toc, toc_fn)

main()
