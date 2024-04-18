# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import flask
from server.api_utils import get_field, get_int, get_json, make_get_json_route, make_post_json_route

import io
import struct

class SectionsEditor(object):
	def __init__(self, state):
		self.state = state

		self.edited_asset = None
		self.edited_asset_name = None

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/sections_editor/make", self.make_editor)

		make_get_json_route(app, "/api/sections_editor/section", self.get_section, False)
		make_get_json_route(app, "/api/sections_editor/strings", self.get_strings, False)

		make_post_json_route(app, "/api/sections_editor/edit_asset", self.prepare_edited_asset)
		make_get_json_route(app, "/api/sections_editor/edited_asset", self.get_edited_asset, False)

	def make_editor(self):
		locator = get_field(flask.request.form, "locator")
		return {"report": self.get_asset_editor(locator)}

	#

	def get_section(self):
		locator = get_field(flask.request.args, "locator")
		section = get_int(flask.request.args, "section")

		data, asset = self.state.get_asset(locator)
		section_data = asset.dat1.get_section(section)._raw
		filename = self.state.get_asset_basename(locator) + ".{:08X}.raw".format(section)

		return flask.send_file(io.BytesIO(section_data), as_attachment=True, download_name=filename, mimetype='application/octet-stream')

	def get_strings(self):
		locator = get_field(flask.request.args, "locator")

		data, asset = self.state.get_asset(locator)
		strings_data = asset.dat1._raw_strings_data
		filename = self.state.get_asset_basename(locator) + ".strings.raw"

		return flask.send_file(io.BytesIO(strings_data), as_attachment=True, download_name=filename, mimetype='application/octet-stream')

	#

	def prepare_edited_asset(self):
		rq = flask.request
		locator = get_field(rq.form, "locator")
		header = get_json(rq.form, "header")
		strings = get_json(rq.form, "strings")
		sections = get_json(rq.form, "sections")

		if strings["option"] == "replace":
			strings["raw"] = rq.files["strings_raw"].read()

		for s in sections:
			if s["option"] == "replace":
				s["raw"] = rq.files["{:08X}_raw".format(s["tag"])].read()

		self.edit_asset(locator, header, strings, sections)
		return {}

	def get_edited_asset(self):
		return flask.send_file(self.edited_asset, as_attachment=True, download_name=self.edited_asset_name, mimetype='application/octet-stream')

	# internal

	def get_asset_editor(self, locator):
		data, asset = self.state.get_asset(locator)

		#

		report = {
			"header": {"magic": 0, "size": 0, "rest": []},
			"strings": {"count": 0, "size": 0},
			"sections": [],
			"total_size": len(data)
		}

		#

		report["header"]["magic"], report["header"]["size"] = struct.unpack("<II", data[:8])
		report["header"]["rest"] = [struct.unpack("<I", data[8+i*4:12+i*4])[0] for i in range(7)]

		report["strings"]["count"] = len(asset.dat1._strings_map)
		report["strings"]["size"] = len(asset.dat1._raw_strings_data)

		#

		sorted_sections = [(s.tag, s.offset, s.size) for s in asset.dat1.header.sections]
		sorted_sections = sorted(sorted_sections, key=lambda x: x[1])

		for tag, _, size in sorted_sections:
			# TODO: web_editor_data()
			report["sections"] += [{"tag": tag, "size": size, "type": "raw"}]

		#

		return report

	def edit_asset(self, locator, header, strings, sections):
		_, asset = self.state.get_asset(locator) # a new copy instead of reusing existing one, because we're editing it
		dat1 = asset.dat1

		if strings["option"] == "replace":
			dat1._raw_strings_data = strings["raw"]
		
		elif strings["option"] == "append":
			lines = strings["appended"].replace('\r\n', '\n').replace('\r', '\n').split('\n')
			for l in lines:
				dat1.add_string(l)

		#

		index = 0
		for s in sections:
			tag = s["tag"]
			option = s["option"]

			for hs in dat1.header.sections:
				if hs.tag == tag:
					hs.offset = index
					break
			index += 1

			if option == "replace":
				dat1._sections_data[dat1._sections_map[tag]] = s["raw"]

		dat1.recalculate_section_headers()		

		#

		f = io.BytesIO(bytes())

		magic, size = int(header["magic"]), int(header["size"])
		if header["recalculate_size"]:
			size = dat1.header.size
		f.write(struct.pack("<II", magic, size))

		rest = header["rest"]
		for x in rest:
			f.write(struct.pack("<I", int(x)))

		dat1.save(f)
		f.seek(0)

		self.edited_asset = f
		self.edited_asset_name = self.state.get_asset_basename(locator)
