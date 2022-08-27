import struct
import math
import string
import os
import os.path

import sys
import os
import os.path
import re

import dat1lib
import dat1lib.types.dag
import dat1lib.types.dat1
import dat1lib.types.model
import dat1lib.types.toc
import dat1lib.utils

import dat1lib.types.sections.toc.archives

import dat1lib

def print_table(arr, fmt, entries_per_line):
	s = ""
	cnt = 0
	for x in arr:
		if s == "":
			s = "-"
		s += fmt.format(x)
		cnt += 1
		if cnt == entries_per_line:
			print s
			s = ""
			cnt = 0
	if s != "":
		print s

####

DEBUG_PRINT_SECTIONS = True
DEBUG_PRINT_SECTIONS_VERBOSE = True

def true_or_none(x):
	return (x is None or x)

def format_bytes(bytes_arr):
	return " ".join(["{:02X}".format(x) for x in bytes_arr])

def treat_as_bytes(num_bytes, strct):
	bts = struct.unpack("<" + ("B" * num_bytes), strct)
	return format_bytes(bts)

def print_info(obj):
	if isinstance(obj, dat1lib.types.model.Model):
		print "-------"
		print "Model {:08X}".format(obj.magic)
		if obj.magic != dat1lib.types.model.Model.MAGIC:
			print "[!] Unknown magic, should be {}".format(dat1lib.types.model.Model.MAGIC)
		print ""
		print "Streaming part:"
		print "- offset = {}".format(obj.offset_to_stream_sections)
		print "- size   = {}".format(obj.stream_sections_size)
		if False:
			print ""
			print treat_as_bytes(12, obj.unk[:12])
			print treat_as_bytes(12, obj.unk[12:])
		print "-------"
		print ""

		print_info(obj.dat1)
		return

	if isinstance(obj, dat1lib.types.toc.TOC):
		print "-------"
		# TODO: toc
		print "-------"
		print ""

		print_info(obj.dat1)
		return

	####

	print "-------"
	
	suffix = ""
	UNK1_KNOWN_VALUES = {
		0x98906B9F: "model",
		0x2A077A51: "dag",
		0x51B8E006: "toc"
	}
	if obj.header.unk1 in UNK1_KNOWN_VALUES:
		suffix = " ({})".format(UNK1_KNOWN_VALUES[obj.header.unk1])

	print "DAT1 {:08X}{}".format(obj.header.unk1, suffix)
	if obj.header.magic != 0x44415431:
		print "[!] Unknown magic, should be 0x44415431"
	print "-------"

	# obj

	if true_or_none(DEBUG_PRINT_SECTIONS):
		print ""
	
	print "Sections: {}".format(len(obj.header.sections))

	if true_or_none(DEBUG_PRINT_SECTIONS) and len(obj.header.sections) > 0:
		print "-------------------------------------------"
		#######  12 12345678  12345678  12345678  12345678
		print "  #  `tag`       offset      size   ends at"
		print "-------------------------------------------"
		for i, section_header in enumerate(obj.header.sections):
			print "- {:<2} {:08X}  {:8}  {:8}  {:8}".format(i, section_header.tag, section_header.offset, section_header.size, section_header.offset + section_header.size - 1)

		if true_or_none(DEBUG_PRINT_SECTIONS_VERBOSE):
			first_section = True
			for i, section_header in enumerate(obj.header.sections):
				section = obj.sections[i]
				if section is not None:
					if first_section:
						print ""
						first_section = False

					if False and section_header.tag == dat1lib.SECTION_SIZE_ENTRIES:
						print "{:08X} | Size Entries | {:6} entries".format(section_header.tag, len(section.entries))
						had_warnings = False
						for j, e in enumerate(section.entries):
							if j != e.index:
								print "    [!] #{} bad index: {}".format(j, e.index)
								had_warnings = True
							if e.always1 != 1:
								print "    [!] #{} always1 == {}".format(j, e.always1)
								had_warnings = True
						if had_warnings:
							print ""
					elif section_header.tag == dat1lib.types.sections.toc.archives.ArchivesSection.TAG:
						print "{:08X} | Archives Map | {:6} entries".format(section_header.tag, len(section.archives))
					elif False and section_header.tag == dat1lib.SECTION_ASSET_IDS:
						print "{:08X} | Asset IDs    | {:6} entries".format(section_header.tag, len(section.ids))
						"""
						for aid in section.ids:
							if aid == 9767039763554194594: # 9223475264534229424: # 9223384287010557067:
								print "!!! found !!!"
								break
						"""
					elif False and section_header.tag == dat1lib.SECTION_KEY_ASSETS:
						print "{:08X} | Key Assets   | {:6} entries".format(section_header.tag, len(section.ids))
					elif False and section_header.tag == dat1lib.SECTION_OFFSET_ENTRIES:
						print "{:08X} | Offsets      | {:6} entries".format(section_header.tag, len(section.entries))
						"""
						files_per_archive = {}
						for e in section.entries:
							files_per_archive[e.archive_index] = files_per_archive.get(e.archive_index, 0) + 1
						print files_per_archive
						"""
					elif False and section_header.tag == dat1lib.SECTION_SPAN_ENTRIES:
						print "{:08X} | Spans        | {:6} entries".format(section_header.tag, len(section.entries))
						"""
						for e in section.entries:
							print e.asset_index, e.count
						"""

def main(argv):
	if len(argv) < 2:
		print "Usage:"
		print "$ {} <filename>".format(argv[0])
		print ""
		print "Read the file (could be 'toc', 'dag', '.model' or any '1TAD')"
		print "and print as much info about it as possible"
		return

	#

	fn = argv[1]
	obj = None
	try:
		with open(fn, "rb") as f:
			obj = dat1lib.read(f)
	except Exception as e:
		print "[!] Couldn't open '{}'".format(fn)
		print e
		return

	#
	
	if obj is None:
		print "[!] Couldn't comprehend '{}'".format(fn)
		return
	
	print_info(obj)

if __name__ == "__main__":
	main(sys.argv)	
