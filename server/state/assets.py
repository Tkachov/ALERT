import flask
from server.api_utils import get_int, make_get_json_route, make_post_json_route

import io

class Assets(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/assets/get_info", self.get_info)
		make_get_json_route(app, "/api/assets/asset", self.get_asset, False)

	def get_info(self):
		index = get_int(flask.request.form, "index")

		asset, sz, thumbnail = self.state.extract_asset(index)

		info = {"type": None, "magic": None, "sections": None, "size": sz}
		if asset is not None:
			info = {
				"type": asset.__class__.__name__,
				"magic": asset.MAGIC,
				"sections": len(asset.dat1.sections),
				"size": sz
			}

		return {"asset": info, "thumbnail": thumbnail}

	def get_asset(self):
		index = get_int(flask.request.args, "index")

		data, asset = self.state._get_asset_by_index(index)
		filename = self.state._get_asset_name(index)

		return flask.send_file(io.BytesIO(data), as_attachment=True, download_name=filename, mimetype='application/octet-stream')
