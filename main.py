import sys
import os
import os.path
import re

import dat1lib
import dat1lib.utils
import info_printer

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

	return (f, is_model)

def main():
	f, is_model = handle_args()
	model_header, dat1 = dat1lib.read(f, is_model)
	info_printer.print_info(model_header, dat1)

if __name__ == "__main__":
	main()
