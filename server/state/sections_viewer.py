import flask
from server.api_utils import get_int, make_post_json_route

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
		index = get_int(flask.request.form, "index")
		return {"report": self.get_asset_report(index)}

	# internal

	def get_asset_report(self, index):
		data, asset = self.state._get_asset_by_index(index)

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
			try:
				if section is not None:
					if "web_repr" in dir(section):
						report["sections"][s.tag] = section.web_repr()
					else:
						captured = io.StringIO()
						sys.stdout = captured
						section.print_verbose(CONFIG)
						report["sections"][s.tag] = {"name": "{:08X}".format(s.tag), "type": "text", "readonly": True, "content": captured.getvalue()}
						sys.stdout = sys.__stdout__

						try:
							if report["sections"][s.tag]["content"] == "": # TODO: make it part of web_repr()
								report["sections"][s.tag]["type"] = "bytes"
								report["sections"][s.tag]["offset"] = 0 # TODO: make it absolute, not section-relative
								report["sections"][s.tag]["content"] = base64.b64encode(section._raw).decode('ascii')
						except:
							pass
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
