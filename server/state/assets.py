import flask
from server.api_utils import get_field, make_get_json_route, make_post_json_route

import io

class Assets(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/assets/get_info", self.get_info)
		make_get_json_route(app, "/api/assets/asset", self.get_asset, False)

	def get_info(self):
		locator = get_field(flask.request.form, "locator")

		asset, thumbnail = self.state.get_asset_with_thumbnail(locator)

		info = {"type": None, "magic": None, "sections": None}
		if asset is not None:
			info = {
				"type": asset.__class__.__name__,
				"magic": asset.MAGIC,
				"sections": len(asset.dat1.sections)
			}

		return {"asset": info, "thumbnail": thumbnail}

	def get_asset(self):
		locator = get_field(flask.request.args, "locator")

		data, asset = self.state.get_asset(locator)
		filename = self.state.get_asset_basename(locator)

		return flask.send_file(io.BytesIO(data), as_attachment=True, download_name=filename, mimetype='application/octet-stream')
