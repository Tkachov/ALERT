import struct
import math
import string
import os
import os.path

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

DEBUG_PRINTS = True
DEBUG_PRINT_SECTIONS = True
DEBUG_PRINT_SECTIONS_VERBOSE = True

def true_or_none(x):
	return (x is None or x)

def format_bytes(bytes_arr):
	return " ".join(["{:02X}".format(x) for x in bytes_arr])

def print_as_bytes(num_bytes, strct):
	bts = struct.unpack("<" + ("B" * num_bytes), strct)
	return format_bytes(bts)

def print_info(model_header, dat1):
	if not DEBUG_PRINTS:
		return

	if model_header is not None:
		print "-------"
		print "Model {:08X}".format(model_header.magic)
		if model_header.magic != 0x98906B9F:
			print "[!] Unknown magic, should be 0x98906B9F"
		print ""
		print_table(model_header.data, " {:08X}", 4)
		print "-------"
		print ""

	####

	print "-------"
	
	suffix = ""
	UNK1_KNOWN_VALUES = {
		0x98906B9F: "model",
		0x2A077A51: "dag",
		0x51B8E006: "toc"
	}
	if dat1.header.unk1 in UNK1_KNOWN_VALUES:
		suffix = " ({})".format(UNK1_KNOWN_VALUES[dat1.header.unk1])

	print "DAT1 {:08X}{}".format(dat1.header.unk1, suffix)
	if dat1.header.magic != 0x44415431:
		print "[!] Unknown magic, should be 0x44415431"
	print "-------"

	# obj

	if true_or_none(DEBUG_PRINT_SECTIONS):
		print ""
	
	print "Sections: {}".format(len(dat1.header.sections))

	if true_or_none(DEBUG_PRINT_SECTIONS) and len(dat1.header.sections) > 0:
		print "-------------------------------------------"
		#######  12 12345678  12345678  12345678  12345678
		print "  #  `tag`       offset      size   ends at"
		print "-------------------------------------------"
		for i, section_header in enumerate(dat1.header.sections):
			print "- {:<2} {:08X}  {:8}  {:8}  {:8}".format(i, section_header.tag, section_header.offset, section_header.size, section_header.offset + section_header.size - 1)

		if true_or_none(DEBUG_PRINT_SECTIONS_VERBOSE):
			first_section = True
			for i, section_header in enumerate(dat1.header.sections):
				section = dat1.sections[i]
				if section is not None:
					if first_section:
						print ""
						first_section = False

					if section_header.tag == dat1lib.SECTION_SIZE_ENTRIES:
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
					elif section_header.tag == dat1lib.SECTION_ARCHIVES_MAP:
						print "{:08X} | Archives Map | {:6} entries".format(section_header.tag, len(section.archives))
					elif section_header.tag == dat1lib.SECTION_ASSET_IDS:
						print "{:08X} | Asset IDs    | {:6} entries".format(section_header.tag, len(section.ids))
						"""
						for aid in section.ids:
							if aid == 9767039763554194594: # 9223475264534229424: # 9223384287010557067:
								print "!!! found !!!"
								break
						"""
					elif section_header.tag == dat1lib.SECTION_KEY_ASSETS:
						print "{:08X} | Key Assets   | {:6} entries".format(section_header.tag, len(section.ids))
					elif section_header.tag == dat1lib.SECTION_OFFSET_ENTRIES:
						print "{:08X} | Offsets      | {:6} entries".format(section_header.tag, len(section.entries))
						"""
						files_per_archive = {}
						for e in section.entries:
							files_per_archive[e.archive_index] = files_per_archive.get(e.archive_index, 0) + 1
						print files_per_archive
						"""
					elif section_header.tag == dat1lib.SECTION_SPAN_ENTRIES:
						print "{:08X} | Spans        | {:6} entries".format(section_header.tag, len(section.entries))
						"""
						for e in section.entries:
							print e.asset_index, e.count
						"""

def extract_section(dat1, extraction_dir):
	sections = dat1.header.sections
	sections_count = len(sections)

	if sections_count <= 0:
		return

	print ""
	print "Which section do you want to extract? (0-{} or A for all)".format(sections_count-1)
	option = raw_input("> ")
	
	extract_range = None
	if option is not None and len(str(option)) >= 1:
		if str(option).upper()[0] == 'A':
			extract_range = xrange(sections_count)
		else:
			try:
				option = int(option)
				if option >= 0 and option < sections_count:
					extract_range = xrange(option, option + 1)
			except:
				pass

	if extract_range is None:
		print "[!] Bad option {}.".format(repr(option))
		return

	print ""
	if len(extract_range) > 1:
		print "Extracting sections from {} to {}...".format(extract_range[0], extract_range[-1])
	else:
		print "Extracting section #{}...".format(extract_range[0])

	try:
		os.makedirs(extraction_dir)
	except:
		pass

	for i in extract_range:
		section = sections[i]
		fn = extraction_dir + "/{:02}_{:08X}.section".format(i, section.tag)
		print fn
		
		f = open(fn, "wb")
		f.write(dat1._sections_data[i])
		f.close()
