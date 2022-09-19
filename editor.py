import sys

if __name__ == "__main__":
	if len(sys.argv) < 2:
		from server.server import app
		app.run(host='0.0.0.0', port=55555)
	else:
		import main
		main.main(sys.argv)
