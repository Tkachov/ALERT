import sys

if __name__ == "__main__":
	argv = sys.argv
	if len(argv) < 3:
		print("Usage:")
		print("$ {} <.model filename> <.ascii filename> [_materials.txt filename]".format(argv[0]))
		sys.exit(1)

	model_fn = argv[1]
	ascii_fn = argv[2]
	materials_txt = None
	if len(argv) > 3:
		materials_txt = argv[3]
	new_argv = argv[:1] + [ascii_fn, model_fn, materials_txt, model_fn]

	import ascii_to_model
	ascii_to_model.main(new_argv)
