from flask import Flask, url_for, send_from_directory, request, Response
import importlib
from functools import wraps

from state import State

state = State()

app = Flask(__name__)

##### THIS IS MAGIC #####

def renamer(name):
	def actual_dec(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			return f(*args, **kwargs)
		wrapper.func_name = name
		return wrapper
	return actual_dec

def make_get_route(route, module):
	@app.route(route)
	@renamer('_flask_handler_'+module)
	def decorated(*args, **kwargs):
		md = importlib.import_module(module)
		return md.handle(request, state)
	return decorated

def make_post_route(route, module):
	@app.route(route, methods=['POST'])
	@renamer('_flask_handler_'+module)
	def decorated(*args, **kwargs):
		md = importlib.import_module(module)
		return md.handle(request, state)
	return decorated

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
api_post('search_assets')
api_post('extract_asset')
api_post('asset_report')
api_post('asset_editor')
api_get('model')
api_get('editor.extract')
api_get('editor.save_section')
api_get('editor.save_strings')

#########################

# static stuff

@app.route('/')
def index():
	return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def send_static(path):
	return send_from_directory('static', path)

# error handling

def get_file_contents(filename):
	f = open(filename, 'r')
	res = f.read()
	f.close()
	return res

@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def http_error_handler(error):	
	return get_file_contents('static/%d.html' % error.code), error.code
