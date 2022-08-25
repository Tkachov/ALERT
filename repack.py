import struct
import math
import string
import os
import os.path
import json
import io
import zlib
import sys

import dat1lib

class ModelHeader(object):
	def __init__(self, f):
		self.magic, = dat1lib.utils.read_struct(f, "<I")
		self.data = list(dat1lib.utils.read_struct(f, "<" + "I"*8))

###

def main(argv):
	if len(argv) < 2:
		print "Usage:"
		print "$ {} <filename>".format(argv[0])
		print ""
		print "Read the .model and save it as .model.repacked"
		print "Resulting file should work in game as usual"
		return

	#

	fn = argv[1]
	f = None
	try:
		f = open(fn, "rb")
	except:
		print "[!] Couldn't open '{}'".format(fn)
		return

	#

	model_header = ModelHeader(f)
	offset = 36
	
	dat1 = dat1lib.DAT1(f, offset)
	f.close()

	dat1.set_recalculation_strategy(dat1lib.RECALCULATE_ORIGINAL_ORDER)
	dat1.recalculate_section_headers()

	f = open(fn + ".repacked", "wb")
	f.write(struct.pack("<I", model_header.magic))

	offset_to_indexbuf = 0
	for s in dat1.header.sections:
		if s.tag == 0x0859863D:
			offset_to_indexbuf = s.offset

	model_header.data[0] = offset_to_indexbuf
	model_header.data[1] = dat1.header.size - offset_to_indexbuf

	f.write(struct.pack("<" + "I"*8, *model_header.data))
	dat1.save(f)
	f.close()

if __name__ == "__main__":
	main(sys.argv)
