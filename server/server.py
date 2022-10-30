import sys
import os
from flask import Flask, url_for, send_from_directory, request, Response
import importlib
from functools import wraps

from server.state import State

state = State()
app = None

def print_self(filename):
	try:
		from pefile import PE

		name = None
		version = None

		pe = PE(filename)
		for i in range(len(pe.FileInfo)):
			try:
				fi = pe.FileInfo[i]
				for j in range(len(fi)):
					try:
						content = fi[j]
						sts = content.StringTable
						for st in sts:
							for k, v in st.entries.items():
								if k == b"ProductName":
									name = v
								elif k == b"ProductVersion":
									version = v
					except:
						pass
			except:
				pass

		if name is not None:
			if version is not None:
				print(" * {} v. {}".format(name.decode('ascii'), version.decode('ascii')))
			else:
				print(" *", name)
	except:
		pass

if getattr(sys, 'frozen', False):
	print_self(sys.argv[0])
	print(" *", sys._MEIPASS)
	print("")
	app = Flask(__name__, static_folder=os.path.join(sys._MEIPASS, 'static'))
else:
	app = Flask(__name__)

def make_get_route(route, module):
	decorated = lambda *args, **kwargs: importlib.import_module(module).handle(request, state)
	decorated.__name__ = '_flask_handler_'+module
	app.add_url_rule(route, view_func=decorated)

def make_post_route(route, module):
	decorated = lambda *args, **kwargs: importlib.import_module(module).handle(request, state)
	decorated.__name__ = '_flask_handler_'+module
	app.add_url_rule(route, methods=['POST'], view_func=decorated)

PREFIX = "api." # gunicorn
PREFIX = "server.api." # for Flask

def api_get(module):
	route = '/'.join(module.split('.'))
	make_get_route('/api/' + route, PREFIX + module)

def api_post(module):
	route = '/'.join(module.split('.'))
	make_post_route('/api/' + route, PREFIX + module)

#########################

# API

api_post('load_toc')
api_post('extract_asset')
api_post('asset_report')
api_post('asset_editor')
api_get('model')
api_get('editor.edited_asset')
api_get('editor.extract')
api_get('editor.save_section')
api_get('editor.save_strings')
api_post('editor.edit_asset')
api_post('thumbnails.list')
api_get('thumbnails.get')
api_post('textures.viewer')
api_get('textures.get')

#########################

# static stuff

@app.route('/')
def index():
	return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def send_static(path):
	r = send_from_directory(app.static_folder, path)
	
	ct = None
	if path.endswith(".js"):
		ct = "application/javascript; charset=utf-8"
	elif path.endswith(".ico"):
		ct = "image/x-icon"

	if ct is not None:
		r.headers['Content-Type'] = ct

	return r

# error handling

@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def http_error_handler(error):	
	return send_from_directory(app.static_folder, "%d.html" % error.code), error.code
