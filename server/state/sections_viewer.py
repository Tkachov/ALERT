import flask
from server.api_utils import get_field, make_post_json_route

import base64
import io
import sys

class SectionsViewer(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/sections_viewer/make", self.make_viewer)

	def make_viewer(self):
		locator = get_field(flask.request.form, "locator")
		return {"report": self.get_asset_report(locator)}

	# internal

	def get_asset_report(self, locator):
		data, asset = self.state.get_asset(locator)

		report = {"header": [], "sections": {}, "strings": ""}
		report["header"] = [(s.tag, s.offset, s.size) for s in asset.dat1.header.sections]

		#
		
		CONFIG = {
			"sections": True,
			"sections_verbose": True,
			"web": True
		}

		for ndx, s in enumerate(asset.dat1.header.sections):
			section = asset.dat1.sections[ndx]
			report["sections"][s.tag] = ""
			content_set = False

			try:
				if section is not None:
					if "web_repr" in dir(section):
						report["sections"][s.tag] = section.web_repr()
						content_set = True
					else:
						captured = io.StringIO()
						sys.stdout = captured
						section.print_verbose(CONFIG)
						report["sections"][s.tag] = {"name": "{:08X}".format(s.tag), "type": "text", "readonly": True, "content": captured.getvalue()}
						sys.stdout = sys.__stdout__
						content_set = True

						if report["sections"][s.tag]["content"] == "":
							content_set = False
			except:
				pass

			try:
				if not content_set:
					if report["sections"][s.tag] == "":
						report["sections"][s.tag] = {"name": "{:08X}".format(s.tag), "type": "", "readonly": True, "content": ""}
					
					report["sections"][s.tag]["type"] = "bytes"
					report["sections"][s.tag]["offset"] = s.offset
					report["sections"][s.tag]["content"] = base64.b64encode(asset.dat1._sections_data[ndx]).decode('ascii')
			except:
				pass

		#

		try:
			items = asset.dat1._strings_map.items()
			items = sorted(items, key=lambda x: x[0])
			########## 123  123456  ...
			result =  "#    offset  value\n"
			result += "------------------\n"
			for i, (offset, s) in enumerate(items):
				result += "{:<3}  {:6}  {}\n".format(i, offset, repr(s))
			report["strings"] = result
		except:
			pass

		#

		return report
