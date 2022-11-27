import flask
from server.api_utils import get_field, get_int, get_json, make_get_json_route, make_post_json_route

import dat1lib.types.sections
import dat1lib.types.sections.config.serialized
import dat1lib.types.sections.config.references
import io
import struct

#

class EditableSerialized(dat1lib.types.sections.SerializedSection):
	def __init__(self, data, container):
		super().__init__(data, container)

	@classmethod
	def read(cls, config, section_tag):
		data = config.dat1.get_section(section_tag)._raw
		s = EditableSerialized(data, config.dat1)
		return s.root

	def _deserialize(self, f):
		return self._deserialize_node(f, self.NT_OBJECT)

	def _deserialize_array(self, f, item_type, items_count):
		return {"type": -1, "value": [self._deserialize_node(f, item_type) for i in range(items_count)]}

	def _deserialize_node(self, f, item_type):
		v = super()._deserialize_node(f, item_type)

		if item_type == self.NT_STRING:
			v, h64 = v
			return {"type": item_type, "value": v, "string_hash": "{:016X}".format(h64)}
		
		if item_type == self.NT_INSTANCE_ID:
			v = "{:016X}".format(v)

		return {"type": item_type, "value": v}

	def _deserialize_string(self, f):
		length, h32, h64 = struct.unpack("<IIQ", f.read(16))
		v = f.read(length)
		f.read(1) # nullbyte
		self._align(f, 4)
		return v.decode('ascii'), h64

#

class ConfigsEditor(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/configs_editor/make", self.make_editor)

		"""
		make_post_json_route(app, "/api/sections_editor/edit_asset", self.prepare_edited_asset)
		make_get_json_route(app, "/api/sections_editor/edited_asset", self.get_edited_asset, False)
		"""

	def make_editor(self):
		locator = get_field(flask.request.form, "locator")
		return self.get_config_editor(locator)

	"""
	def prepare_edited_asset(self):
		rq = flask.request
		index = get_int(rq.form, "index")
		header = get_json(rq.form, "header")
		strings = get_json(rq.form, "strings")
		sections = get_json(rq.form, "sections")

		if strings["option"] == "replace":
			strings["raw"] = rq.files["strings_raw"].read()

		for s in sections:
			if s["option"] == "replace":
				s["raw"] = rq.files["{:08X}_raw".format(s["tag"])].read()

		self.edit_asset(index, header, strings, sections)
		return {}

	def get_edited_asset(self):
		return flask.send_file(self.edited_asset, as_attachment=True, download_name=self.edited_asset_name, mimetype='application/octet-stream')
	"""

	# internal

	def get_config_editor(self, locator):
		data, asset = self.state.get_asset(locator)

		s = asset.dat1.get_section(dat1lib.types.sections.config.references.ReferencesSection.TAG)
		refs = []
		if s is not None:
			refs = [("{:016X}".format(x[0]), asset.dat1.get_string(x[1])) for x in s.entries]

		editor = {
			"type": EditableSerialized.read(asset, dat1lib.types.sections.config.serialized.ConfigTypeSection.TAG),
			"content": EditableSerialized.read(asset, dat1lib.types.sections.config.serialized.ConfigContentSection.TAG),
			"references": refs
		}

		return editor
