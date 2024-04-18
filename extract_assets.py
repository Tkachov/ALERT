# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib
import dat1lib.types.toc
import os
import sys
import traceback

def main(argv):
	if len(argv) < 2:
		print("Usage:")
		print("$ {} <asset_archive path>".format(argv[0]))
		print("")
		print("Interactive assets extractor.")
		return

	#

	asset_archive_path = argv[1]
	toc_fn = os.path.join(asset_archive_path, "toc")
	toc = None
	try:
		with open(toc_fn, "rb") as f:
			toc = dat1lib.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(toc_fn))
		print(e)
		return

	#
	
	if toc is None:
		print("[!] Couldn't comprehend '{}'".format(toc_fn))
		return

	if not isinstance(toc, dat1lib.types.toc.TOC):
		print("[!] Not a toc")
		return
	
	#

	archs = toc.get_archives_section()
	aids = toc.get_assets_section() # lul
	print("TOC: {} archives, {} assets".format(len(archs.archives), len(aids.ids)))
	toc.set_archives_dir(asset_archive_path)

	while True:
		print("")
		aid = input("Enter asset id to extract: ")

		if aid is None or aid == "":
			break

		try:
			aid = int(aid, 16)
		except:
			print("[!] Invalid input, try again")
			continue

		entries = toc.get_asset_entries_by_assetid(aid)
		if len(entries) == 0:
			print("[!] Asset {:016X} not found".format(aid))
			continue

		entry = entries[0]
		if len(entries) > 1:
			print("[i] {} entries for {:016X} were found, first one was selected".format(len(entries), aid))

		try:
			data = toc.extract_asset(entry)
			with open("{:016X}".format(aid), "wb") as f:
				f.write(data)
			print("{:016X} extracted ({} bytes written)".format(aid, len(data)))
		except Exception as e:
			print("[!] Failed")
			print(e)
			print(traceback.format_exc())

if __name__ == "__main__":
	main(sys.argv)	
