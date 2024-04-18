# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import flask
from server.api_utils import get_field, make_get_json_route, make_post_json_route

import dat1lib.decompression as decompression
import io
import struct

class Assets(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/assets/get_info", self.get_info)
		make_get_json_route(app, "/api/assets/asset", self.get_asset, False)
		make_get_json_route(app, "/api/assets/asset_decompressed", self.get_asset_decompressed, False)

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

		data = self.state.get_asset_data(locator)
		filename = self.state.get_asset_basename(locator)

		return flask.send_file(io.BytesIO(data), as_attachment=True, download_name=filename, mimetype='application/octet-stream')

	def get_asset_decompressed(self):
		locator = get_field(flask.request.args, "locator")

		data = self.state.get_asset_data(locator)
		filename = self.state.get_asset_basename(locator)

		def _decompress(data):
			result = io.BytesIO()
			result.write(data[:36])

			decompress = False
			DAT1_MAGIC = 0x44415431
			normal_magic = struct.unpack("<I", data[36:40])[0]
			if normal_magic != DAT1_MAGIC:
				compressed_magic = struct.unpack("<I", data[38:42])[0]
				if compressed_magic == DAT1_MAGIC:
					decompress = True

			if decompress:
				real_size = struct.unpack("<I", data[4:8])[0] # 46:50
				decompressed_data = decompression.decompress(data[36:], real_size)
				result.write(decompressed_data)
			else:
				result.write(data[36:])

			result.seek(0)
			return result

		return flask.send_file(_decompress(data), as_attachment=True, download_name=filename, mimetype='application/octet-stream')
