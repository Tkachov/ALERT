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

def handle_args():
	if len(sys.argv) < 2:
		print "Usage:"
		print "{} <filename>".format(sys.argv[0])
		sys.exit()

	fn = sys.argv[1]
	f = None
	try:
		f = open(fn, "rb")
	except:
		print "Couldn't open '{}'!".format(fn)
		sys.exit()

	return f

def main():
	f = handle_args()

	model_header = ModelHeader(f)
	offset = 36
	
	dat1 = dat1lib.DAT1(f, offset)
	f.close()

	dat1.set_recalculation_strategy(dat1lib.RECALCULATE_ORIGINAL_ORDER)
	dat1.recalculate_section_headers()

	f = open(sys.argv[1] + ".repacked", "wb")
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

main()
