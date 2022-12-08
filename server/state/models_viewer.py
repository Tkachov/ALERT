import flask
from server.api_utils import get_field, get_int, make_get_json_route

import io
import server.mtl_writer
import server.obj_writer

class ModelsViewer(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_get_json_route(app, "/api/models_viewer/mtl", self.get_mtl, False)
		make_get_json_route(app, "/api/models_viewer/obj", self.get_obj, False)

	def get_mtl(self):
		locator = get_field(flask.request.args, "locator")
		locator = self.state.locator(locator)
		_, model = self.state.get_asset(locator)
		return (server.mtl_writer.write(model, locator.stage, self.state), 200)

	def get_obj(self):
		locator = get_field(flask.request.args, "locator")
		looks = get_field(flask.request.args, "looks")
		looks = [int(x) for x in looks.split(",")]
		lod = get_int(flask.request.args, "lod")

		data, asset = self.state.get_asset(locator)
		return (server.obj_writer.write(asset, looks, lod), 200)
