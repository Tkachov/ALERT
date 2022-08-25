import sys

import info
import repack
import inject
import install

def main(argv):
	if len(argv) < 2:
		print "Usage:"
		print "$ {} [script] [args]".format(argv[0])
		print ""
		print "Scripts:"
		print "  info    \t Print as much info about a file as possible"
		print "  repack  \t Read the .model and save it as .model.repacked"
		print "  inject  \t Save the .model as hero.mod and add it to 'toc'"
		print "  install \t Install all MOD0 mods on top of 'toc.orig'"
		print ""
		print "Default script is 'info'"
		return

	#

	scripts = {
		"info": info.main,
		"repack": repack.main,
		"inject": inject.main,
		"install": install.main
	}

	if argv[1] in scripts:
		name = argv[1]
		entry_point = scripts[name]
		entry_point([name] + argv[2:])
		return

	#

	info.main(argv)

if __name__ == "__main__":
	main(sys.argv)
