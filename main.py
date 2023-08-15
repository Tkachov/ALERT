import sys

import info
import extract_assets
import extract_section
import change_soundbank

def main(argv):
	scripts = {
		"info": info.main,
		"extract_assets": extract_assets.main,
		"extract_section": extract_section.main,
		"change_soundbank": change_soundbank.main
	}

	if len(argv) < 2 or argv[1] not in scripts:
		print("Usage:")
		print("$ {} [script] [args]".format(argv[0]))
		print("")
		print("Scripts:")
		print("  info                Print as much info about a file as possible")
		print("  extract_assets      Interactive assets extractor")
		print("  extract_section     Save a single section as file")
		print("  change_soundbank    Inject .bnk into .soundbank")
		return

	#

	name = argv[1]
	entry_point = scripts[name]
	entry_point([name] + argv[2:])

if __name__ == "__main__":
	main(sys.argv)
