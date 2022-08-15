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
	data = f.read()
	f.close()

	payload = {
		"mod_format_version": 1,
		"mod_version": "1.0.0",
		"author": "Tkachov",
		"name": "Rat Model",
		"description": "test mod similar to Josh's",
		"patch": [
			["R", 9767039763554194594, 0, 79940],
			["R", 13782655929496693878, 0, 79940]
		]
	}
	encoded = json.dumps(payload)

	f = open(sys.argv[2], "wb")
	f.write(data)
	f.write(encoded)
	f.write(struct.pack("<II", MAGIC, len(encoded)))
	f.close()

main()
