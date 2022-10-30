import dat1lib
import dat1lib.types.config
import io
import json
import sys

from dat1lib.types.sections.config.serialized import *

def main(argv):
	if len(argv) < 3:
		print("Usage:")
		print("$ {} <filename> <config type>".format(argv[0]))
		print("")
		print("Reads .json and packs it into .config")
		return

	#

	fn = argv[1]
	data = {}
	try:
		with open(fn, "r") as f:
			data = json.load(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(fn))
		print(e)
		return

	#

	config = dat1lib.types.config.Config.make()
	config.dat1.add_section_obj(ConfigTypeSection.make({"Type": argv[2]}, [], config.dat1))
	config.dat1.add_section_obj(ConfigContentSection.make(data, [], config.dat1))

	#

	with open(fn + ".config", "wb") as f:
		config.save(f)

if __name__ == "__main__":
	main(sys.argv)	
