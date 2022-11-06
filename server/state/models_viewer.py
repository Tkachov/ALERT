import flask
from server.api_utils import get_int, make_get_json_route

import io
import server.obj_writer

class ModelsViewer(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_get_json_route(app, "/api/models_viewer/obj", self.get_obj, False)

	def get_obj(self):
		index = get_int(flask.request.args, "index")
		data, asset = self.state._get_asset_by_index(index)
		return (server.obj_writer.write(asset), 200)
