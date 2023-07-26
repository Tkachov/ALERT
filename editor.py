import sys

if __name__ == "__main__":
	no_args = (len(sys.argv) < 2)
	so_mode = False

	if not no_args:
		so_mode = (sys.argv[1] == "so")

	if no_args or so_mode:
		if so_mode:
			import dat1lib
			dat1lib.VERSION_OVERRIDE = dat1lib.VERSION_SO
		from server.server import app
		app.run(host='0.0.0.0', port=55555)
	else:
		import main
		main.main(sys.argv)
