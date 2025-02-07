# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import argparse
import dat1lib
import dat1lib.types.stg
import io
import struct

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('toc')
	parser.add_argument('aid')
	parser.add_argument('--dir', default="")
	parser.add_argument('--only-data', action='store_true')
	parser.add_argument('-o', default="")
	args = parser.parse_args()

	write_stg = True
	if args.only_data:
		write_stg = False

	output_name = args.aid
	if args.o is not None and args.o != "":
		output_name = args.o

	#

	fn = args.toc
	toc = dat1lib.read_toc(fn)
	
	if toc is None:
		print(f"[!] Couldn't comprehend '{fn}'")
		return

	#

	toc.set_archives_dir(args.dir)

	aid = int(args.aid, 16)
	entry = toc.get_asset_entries_by_assetid(aid, stop_on_first=True)[0]
	data = toc.extract_asset(entry)

	with open(output_name, "wb") as f:
		if write_stg:
			texture_index = -1
			try:
				texture_index = toc.get_texture_asset_ids_section().ids.index(aid)
			except:
				pass

			has_header = (entry.header is not None and len(entry.header) > 0)
			has_texture_meta = (texture_index != -1)
			write_stg = (has_header or has_texture_meta)

			if write_stg:
				stg = dat1lib.types.stg.STG.make()

				stg.flags = 0
				if has_header:
					stg.flags |= dat1lib.types.stg.STG_FLAGS_INSTALL_HEADER
				if has_texture_meta:
					stg.flags |= dat1lib.types.stg.STG_FLAGS_INSTALL_TEXTURE_META

				if has_header:
					stg.header = dat1lib.types.stg.AssetHeader(io.BytesIO(entry.header))

				if has_texture_meta:
					stg.texture_meta = toc.get_texture_meta_section().get_texture_meta(texture_index)

				of = io.BytesIO(bytes())
				stg.save(of)
				of.seek(0)
				stg_header = of.read()
				
				# a bit stupid having to recalculate this, but eh
				_, _, header_size, meta_size = struct.unpack("<IIII", stg_header[:16])
				stg_header_size = 16 + header_size + meta_size
				if header_size % 16 != 0:
					stg_header_size += 16 - (header_size % 16)
				if meta_size % 16 != 0:
					stg_header_size += 16 - (meta_size % 16)

				f.write(stg_header[:stg_header_size])

		f.write(data)

#

if __name__ == "__main__":
	main()
