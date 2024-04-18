# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import flask
from server.api_utils import get_field, make_get_json_route, make_post_json_route

import dat1lib.types.autogen
import json
import os
import os.path
import reconstruct_nodegraph

class NodeGraph(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/nodegraph/load_or_reconstruct", self.load)

	def load(self):
		path = get_field(flask.request.form, "path")

		if os.path.exists(path):
			return {"result": self._load_real_file(path)}
		
		return {"result": self._load_asset(path)}

	# internal

	def _load_real_file(self, path):
		# try loading .nodegraph (w/h reconstruct)
		asset = None
		try:
			with open(path, "rb") as f:
				asset = dat1lib.read(f)
		except Exception as e:
			asset = None

		if asset is not None and isinstance(asset, dat1lib.types.autogen.NodeGraph):
			return reconstruct_nodegraph.reconstruct(asset)

		# if not, maybe it's reconstructed .json?
		with open(path, "rb") as f:
			return json.load(f)

	def _load_asset(self, locator):
		# try loading .nodegraph (w/h reconstruct)
		locator = self.state.locator(locator)
		data, asset = self.state.get_asset(locator)

		if asset is not None and isinstance(asset, dat1lib.types.autogen.NodeGraph):
			return reconstruct_nodegraph.reconstruct(asset)

		# if not, maybe it's reconstructed .json?
		return json.loads(data)
