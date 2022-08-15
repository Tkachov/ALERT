import sys
import os
import os.path
import re

import zlib
import io
import struct

import dat1lib
import dat1lib.utils
import info_printer
import mod_toc

class ModelHeader(object):
	def __init__(self, f):
		self.magic, = dat1lib.utils.read_struct(f, "<I")
		self.data = dat1lib.utils.read_struct(f, "<" + "I"*8)

###

def handle_args():
	if len(sys.argv) < 2:
		print "Usage:"
		print "{} <filename> [directory to extract to]".format(sys.argv[0])
		sys.exit()

	fn = sys.argv[1]
	f = None
	try:
		f = open(fn, "rb")
	except:
		print "Couldn't open '{}'!".format(fn)
		sys.exit()

	is_model = (".model" in fn)

	extraction_dir = os.path.basename(fn).replace(".model", "") + "_extracted"
	if len(sys.argv) > 2:
		extraction_dir = sys.argv[2]

	return (f, is_model, extraction_dir)

def main():
	f, is_model, extraction_dir = handle_args()

	magic, = struct.unpack("<I", f.read(4))
	f.seek(0)
	if magic == 0x77AF12AF or magic == 0x891F77AF:
		# compressed toc
		is_model = False
		is_toc = (magic == 0x77AF12AF)
		print "compressed {} detected".format("toc" if is_toc else "dag")

		f.seek(4)
		size, = struct.unpack("<I", f.read(4))
		if not is_toc:
			f.read(4) # unknown 4 bytes
		dec = zlib.decompressobj(0)
		data = dec.decompress(f.read())
		f.close()

		print "real decompressed size = {}".format(len(data))

		f = io.BytesIO(data)
		if len(data) != size:
			print "[!] Actual decompressed size {} isn't equal to one written in the file {}".format(len(data), size)
		print ""

	model_header = None
	offset = 0
	if is_model:
		model_header = ModelHeader(f)
		offset = 36
	
	dat1 = dat1lib.DAT1(f, offset)
	f.close()

	info_printer.print_info(model_header, dat1)
	# info_printer.extract_section(dat1, extraction_dir)
	mod_toc.do_mod(dat1, "toc.mod")

main()
