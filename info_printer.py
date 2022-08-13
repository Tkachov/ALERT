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

def extract_secion(dat1, extraction_dir):
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
		f.write(dat1.sections_data[i])
		f.close()
