import dat1lib
import dat1lib.crc64 as crc64
import dat1lib.types.toc
import dat1lib.types.sections.toc.archives
import dat1lib.types.sections.toc.asset_ids
import dat1lib.types.sections.toc.offsets
import dat1lib.types.sections.toc.sizes
import os
import os.path
import shutil
import sys

SECTION_ARCHIVES_MAP = dat1lib.types.sections.toc.archives.ArchivesSection.TAG
SECTION_ASSET_IDS = dat1lib.types.sections.toc.asset_ids.AssetIdsSection.TAG
SECTION_OFFSET_ENTRIES = dat1lib.types.sections.toc.offsets.OffsetsSection.TAG
SECTION_SIZE_ENTRIES = dat1lib.types.sections.toc.sizes.SizesSection.TAG

#

def recursive_files_list(d):
	result = []

	for root, subdirs, files in os.walk(d):
		result += [os.path.join(root, fn) for fn in files]

	return result

def make_files_list(paths):
	files = 0
	dirs = 0
	errors = 0

	result = []

	for p in paths:
		if os.path.isdir(p):
			result += recursive_files_list(p)
			dirs += 1
		elif os.path.exists(p):
			result += [p]
			files += 1
		else:
			files += 1
			errors += 1

	message = ""
	if files > 0:
		message += "{} files".format(files)
	if dirs > 0:
		if message != "":
			message += " and "
		message += "{} directories".format(dirs)
	message += " passed"

	if errors > 0:
		message += ", {} were not found".format(errors)

	result = sorted(list(set(result))) # unique + sort

	print(message)
	print("{} files total".format(len(result)))
	print("")

	return result

def make_internal_names(files):
	result = []

	cwd = os.getcwd()
	cwd = os.path.join(cwd, "")
	for f in files:
		af = os.path.abspath(f)
		wf = os.path.basename(af)
		if af.startswith(cwd):
			wf = af[len(cwd):]
		result += [wf]

	return result

#

def read_toc(fn):
	try:
		with open(fn, "rb") as f:
			toc = dat1lib.read(f)

		if not isinstance(toc, dat1lib.types.toc.TOC):
			print("[!] Not a toc")
			return (False, None)

		return (True, toc)
	except Exception as e:
		print("[!] Exception:", e)
		return (False, None)

	print("[!] Unknown error occurred while reading 'toc'")
	return (False, None)

def new_archive(toc):
	s = toc.dat1.get_section(SECTION_ARCHIVES_MAP)
	new_archive_index = len(s.archives)
	fn = "archive{:03}".format(new_archive_index)
	s.archives += [dat1lib.types.sections.toc.archives.ArchiveFileEntry.make(0, 10000 + new_archive_index, fn)]
	toc.dat1.refresh_section_data(SECTION_ARCHIVES_MAP)
	return (new_archive_index, fn)

def new_offset_entry(archive_index, offset):
	e = dat1lib.types.sections.toc.offsets.OffsetEntry(b"\x00"*8)
	e.archive_index = archive_index
	e.offset = offset
	return e

def new_size_entry(size, index):
	e = dat1lib.types.sections.toc.sizes.SizeEntry(b"\x00"*12)
	e.always1 = 1
	e.value = size
	e.index = index
	return e

def save_toc(toc, fn):
	with open(fn, "wb") as f:
		toc.save(f)

#

def main(argv):
	if len(argv) < 2:
		print("Usage:")
		print("$ {} <file1> [<file2>] [...]".format(argv[0]))
		return

	do_replace = False
	do_verbose = False
	do_interactive = True
	clean_args = []
	for a in argv[1:]:
		if a is None or a == "":
			continue
		if a.startswith("--"):
			# actually, these can be filenames?
			if a == "--replace":
				do_replace = True
			elif a == "--verbose":
				do_verbose = True
			elif a == "--no-interactive":
				do_interactive = False
			continue
		clean_args += [a]

	files = make_files_list(clean_args)
	names = make_internal_names(files)

	# TODO: verbose absolute -> internal

	if len(files) == 0:
		print("[!] No files found")
		return

	#

	toc_orig_fn = "toc.original"
	toc_fn = "toc"
	if not os.path.exists(toc_orig_fn):
		shutil.copyfile(toc_fn, toc_orig_fn)
		print("[i] Made a backup of '{}' in '{}'".format(toc_fn, toc_orig_fn))
		print("")
	
	success, toc = read_toc(toc_fn)
	if not success:
		return

	#

	archives = toc.get_archives_section()
	assets = toc.get_assets_section()
	sizes = toc.get_sizes_section()
	offsets = toc.dat1.get_section(SECTION_OFFSET_ENTRIES)
	print("TOC: {} archives, {} assets".format(len(archives.archives), len(assets.ids)))
	print("")

	existing_assets = {}
	for i in range(len(assets.ids)):
		aid = assets.ids[i]
		if aid not in existing_assets:
			existing_assets[aid] = i

	#

	ndx, fn = new_archive(toc)
	archive_file = open(fn, "wb")

	ids_clashed = []
	replacements = 0

	###### 0123456789 0123456789 0123456789012345  ...
	print("Offset     Size       Asset ID          Name")
	print("-"*79)

	offset = 0
	for f, n in zip(files, names):
		size = 0
		with open(f, "rb") as asset:
			data = asset.read()
			size = len(data)
			archive_file.write(data)

		replace_original_asset = False

		aid = crc64.hash(n)
		if aid in existing_assets:
			ids_clashed += [n]
			if do_replace:
				replacements += 1
				replace_original_asset = True

		print("{:<10} {:<10} {:016X}  {}".format(offset, size, aid, n))

		if replace_original_asset:
			asset_index = existing_assets[aid]
			if do_verbose and False:
				print("\t", sizes.entries[asset_index].value, '=>', size)
				print("\t", offsets.entries[asset_index].archive_index, '=>', ndx)
				print("\t", offsets.entries[asset_index].offset, '=>', offset)

			sizes.entries[asset_index].value = size
			offsets.entries[asset_index].archive_index = ndx
			offsets.entries[asset_index].offset = offset
		else:
			new_index = len(assets.ids)
			assets.ids += [aid]
			sizes.entries += [new_size_entry(size, new_index)]
			offsets.entries += [new_offset_entry(ndx, offset)]
			# TODO: remember it in existing_assets? kinda unlikely that we'd be adding multiple assets with the same hash

		offset += size

	print("")

	message = "{} records added".format(len(files) - replacements)
	if len(ids_clashed) > 0:
		message += ", {} IDs clashes, {} replaced".format(len(ids_clashed), replacements)

	print(message)
	print("")

	if do_verbose:
		print("Clashed files:")
		###### 0123456789012345  ...
		print("Asset ID          Name")
		print("-"*79)
		for fn in ids_clashed:
			print("{:016X}  {}".format(crc64.hash(fn), fn))
		print("")

	archive_file.close()

	#

	toc.dat1.refresh_section_data(SECTION_SIZE_ENTRIES)
	toc.dat1.refresh_section_data(SECTION_OFFSET_ENTRIES)
	toc.dat1.refresh_section_data(SECTION_ASSET_IDS)
	save_toc(toc, toc_fn)

	print("TOC: {} archives, {} assets".format(len(archives.archives), len(assets.ids)))

	#

	if do_interactive:
		print("")
		a = raw_input("Press Enter to close...")

if __name__ == "__main__":
	main(sys.argv)
