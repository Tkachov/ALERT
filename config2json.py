import dat1lib
import dat1lib.types.config
import dat1lib.types.sections.config.serialized
import json
import sys

CONFIG_TYPE_TAG = dat1lib.types.sections.config.serialized.ConfigTypeSection.TAG
CONFIG_CONTENT_TAG = dat1lib.types.sections.config.serialized.ConfigContentSection.TAG

def main(argv):
	if len(argv) < 2:
		print("Usage:")
		print("$ {} <filename>".format(argv[0]))
		print("")
		print("Extracts .config content section and saves as .json")
		return

	#

	fn = argv[1]
	config = None
	try:
		with open(fn, "rb") as f:
			config = dat1lib.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(fn))
		print(e)
		return

	#
	
	if config is None:
		print("[!] Couldn't comprehend '{}'".format(fn))
		return

	if not isinstance(config, dat1lib.types.config.Config):
		print("[!] Not a .config")
		return

	#

	s = config.dat1.get_section(CONFIG_TYPE_TAG)
	if s is None:
		print("[!] .config type section is missing")
		return

	print("Type: {}".format(s.root["Type"]))

	#

	s = config.dat1.get_section(CONFIG_CONTENT_TAG)
	if s is None:
		print("[!] .config content section is missing")
		return

	j = json.dumps(s.root, indent=4)
	with open(fn + ".json", "w") as f:
		f.write(j)

if __name__ == "__main__":
	main(sys.argv)	
