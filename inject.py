# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

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
						print("[!] Asset {:X} not found".format(asset_id))
						return False

					print(sizes.entries[asset_index].value, '=>', asset_size)
					print(offsets.entries[asset_index].archive_index, '=>', archive_index)
					print(offsets.entries[asset_index].offset, '=>', archive_offset)

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

SPIDERMAN_BODY = 9767039763554194594

def main(argv):
	if len(argv) < 3:
		print("Usage:")
		print("$ {} <asset_archive_path> <model>".format(argv[0]))
		print("")
		print("Save the model as 'hero.mod' and add it to 'toc'")
		print(".model will replace 'characters/hero/hero_spiderman/hero_spiderman_body.model' ({:X})".format(SPIDERMAN_BODY))
		print("backup of 'toc' will be stored as 'toc.orig'")
		return

	#

	asset_archive_dir = argv[1]
	model_filename = argv[2]

	toc_orig_fn = os.path.join(asset_archive_dir, "toc.orig")
	toc_fn = os.path.join(asset_archive_dir, "toc")
	if not os.path.exists(toc_orig_fn):
		shutil.copyfile(toc_fn, toc_orig_fn)
	
	success, toc = read_toc(toc_orig_fn)
	if not success:
		print("error1")
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
		"patch": [
			["R", SPIDERMAN_BODY, 0, len(data)]
		]
	}

	index = new_archive(toc, fn)
	if not apply_mod_patch(toc, info, index):
		print("error")
	save_toc(toc, toc_fn)

if __name__ == "__main__":
	main(sys.argv)
