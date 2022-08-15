import struct
import math
import string
import os
import os.path
import json
import io
import zlib
import sys

MAGIC = 0x30444F4D # "MOD0"

def main():
	f = open(sys.argv[1], "rb")

	f.seek(-8, io.SEEK_END)
	magic, size = struct.unpack("<II", f.read(8))
	if magic != MAGIC:
		print "[!] non-modded file"
		return

	f.seek(-8 - size, io.SEEK_END)
	data = json.loads(f.read(size))
	print data

	f.close()

main()
