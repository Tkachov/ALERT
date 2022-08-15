import struct
import math
import string
import os
import os.path
import json
import io
import zlib

import dat1lib

def swap_toc(dat1, dst, src, ar_override):
	index_dst = -1
	index_src = -1

	assets = dat1.get_section(dat1lib.SECTION_ASSET_IDS)
	for i, aid in enumerate(assets.ids):
		if aid == dst:
			index_dst = i
		if aid == src:
			index_src = i
		if index_src != -1 and index_dst != -1:
			break

	# print "[{}] = {:X}, [{}] = {:X}".format(index_dst, dst, index_src, src)

	if index_src == -1:
		print "[!] couldn't find src asset {}".format(src)
		return False

	if index_dst == -1:
		print "[!] couldn't find dst asset {}".format(dst)
		return False

	sizes = dat1.get_section(dat1lib.SECTION_SIZE_ENTRIES)
	offsets = dat1.get_section(dat1lib.SECTION_OFFSET_ENTRIES)

	def assign_size(a, b):
		# a.always1 = b.always1
		a.value = b.value
		# a.index = b.index

	def assign_offset(a, b, ar_override):
		print a.archive_index, a.offset, " -> ", b.archive_index, b.offset
		a.archive_index = b.archive_index
		a.offset = b.offset
		if ar_override is not None:
			a.archive_index = ar_override
			a.offset = 0

	assign_size(sizes.entries[index_dst], sizes.entries[index_src])
	assign_offset(offsets.entries[index_dst], offsets.entries[index_src], ar_override)

	return True

def spider_rat(dat1, ar_override):
	# this.SwapModTOC("characters\\hero\\hero_spiderman\\hero_spiderman_body.model", "characters\\ambient\\amb_rat\\amb_rat.model", -1, -1);
	# this.SwapModTOC("characters\\hero\\hero_spiderman_classic\\hero_spiderman_classic.model", "characters\\ambient\\amb_rat\\amb_rat.model", -1, -1);
	swap_toc(dat1, 9767039763554194594, 13270818392121488823, ar_override)
	swap_toc(dat1, 13782655929496693878, 13270818392121488823, ar_override)
	dat1.refresh_section_data(dat1lib.SECTION_SIZE_ENTRIES)
	dat1.refresh_section_data(dat1lib.SECTION_OFFSET_ENTRIES)

def new_archive(dat1):
	s = dat1.get_section(dat1lib.SECTION_ARCHIVES_MAP)
	# s.archives = s.archives[:34] + [dat1lib.ArchiveFileEntry.make(0, 10034, "g00s034")] + s.archives[34:]
	s.archives = s.archives[:34] + [dat1lib.ArchiveFileEntry.make(0, 10034, "rat.mod")] + s.archives[34:]
	# s.archives += [dat1lib.ArchiveFileEntry.make(0, 10046, "g00s034")]
	dat1.refresh_section_data(dat1lib.SECTION_ARCHIVES_MAP)

def do_mod(dat1, fn):
	if dat1.header.unk1 != 0x51B8E006:
		print "bad toc"
		return

	mod_section = dat1.get_section(dat1lib.SECTION_MOD)
	if mod_section is not None:
		print "already modded:"
		print mod_section
		return

	dat1.add_section(dat1lib.SECTION_MOD, json.dumps({"hello": "world"}))

	# spider_rat(dat1, 46) # similar to Josh's
	spider_rat(dat1, 34)
	new_archive(dat1)
	
	of = io.BytesIO(bytes())
	dat1.save(of)
	of.seek(0)
	uncompressed = of.read()

	print "uncompressed size = {}".format(len(uncompressed))

	c = zlib.compressobj()
	compressed = c.compress(uncompressed)
	compressed += c.flush()

	f = open(fn, "wb")
	f.write(struct.pack("<II", 0x77AF12AF, len(uncompressed)))
	f.write(compressed)
	f.close()
