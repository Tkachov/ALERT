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
import dat1lib.types.toc
import dat1lib.types.sections.toc.archives
import dat1lib.types.sections.toc.asset_ids
import dat1lib.types.sections.toc.mod0
import dat1lib.types.sections.toc.offsets
import dat1lib.types.sections.toc.sizes

SECTION_ARCHIVES_MAP = dat1lib.types.sections.toc.archives.ArchivesSection.TAG
SECTION_ASSET_IDS = dat1lib.types.sections.toc.asset_ids.AssetIdsSection.TAG
SECTION_MOD = dat1lib.types.sections.toc.mod0.Mod0Section.TAG
SECTION_OFFSET_ENTRIES = dat1lib.types.sections.toc.offsets.OffsetsSection.TAG
SECTION_SIZE_ENTRIES = dat1lib.types.sections.toc.sizes.SizesSection.TAG

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
		with open(fn, "rb") as f:
			toc = dat1lib.read(f)

		if not isinstance(toc, dat1lib.types.toc.TOC):
			print "[!] Not a toc"
			return (False, None)

		return (True, toc)
	except Exception as e:
		print "[!] Exception:", e
		return (False, None)

	print "[!] Unknown error occurred while reading 'toc'"
	return (False, None)

def new_archive(toc, fn):
	s = toc.dat1.get_section(SECTION_ARCHIVES_MAP)
	new_archive_index = 0
	for a in s.archives:
		if a.install_bucket != 0:
			break
		new_archive_index += 1

	s.archives = s.archives[:new_archive_index] + [dat1lib.types.sections.toc.archives.ArchiveFileEntry.make(0, 10000 + new_archive_index, fn)] + s.archives[new_archive_index:]
	toc.dat1.refresh_section_data(SECTION_ARCHIVES_MAP)

	return new_archive_index

def apply_mod_patch(toc, mod_info, archive_index):
	try:
		assets = toc.dat1.get_section(SECTION_ASSET_IDS)
		sizes = toc.dat1.get_section(SECTION_SIZE_ENTRIES)
		offsets = toc.dat1.get_section(SECTION_OFFSET_ENTRIES)

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

			toc.dat1.refresh_section_data(SECTION_SIZE_ENTRIES)
			toc.dat1.refresh_section_data(SECTION_OFFSET_ENTRIES)

			return True
	except:
		pass

	return False

def save_toc(toc, fn):
	with open(fn, "wb") as f:
		toc.save(f)

def main(argv):
	if len(argv) < 2:
		print "Usage:"
		print "$ {} <asset_archive_path>".format(argv[0])
		print ""
		print "Install all MOD0 mods on top of 'toc.orig'"
		print "backup of 'toc' will be stored as 'toc.orig'"
		return

	#

	asset_archive_dir = argv[1]
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

	mod_section = toc.dat1.get_section(SECTION_MOD)
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

	toc.dat1.add_section(SECTION_MOD, json.dumps(new_mods_info))
	save_toc(toc, toc_fn)

if __name__ == "__main__":
	main(sys.argv)
