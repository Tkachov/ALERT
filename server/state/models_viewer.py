import flask
from server.api_utils import get_field, get_int, make_get_json_route, make_post_json_route

import dat1lib.types.sections.model.look
import dat1lib.types.sections.model.unknowns
import io
import server.mtl_writer
import server.obj_writer

class ModelsViewer(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/models_viewer/make", self.make_viewer)
		make_get_json_route(app, "/api/models_viewer/mtl", self.get_mtl, False)
		make_get_json_route(app, "/api/models_viewer/obj", self.get_obj, False)

	def make_viewer(self):
		locator = get_field(flask.request.form, "locator")
		return {"viewer": self.get_model_viewer(locator)}

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

	#

	def get_model_viewer(self, locator):
		_, model = self.state.get_asset(locator)
		result = {
			"materials": [],
			"looks": [],
			"lods": []
		}

		SECTION_LOOK       = dat1lib.types.sections.model.look.ModelLookSection.TAG
		SECTION_LOOK_BUILT = dat1lib.types.sections.model.look.ModelLookBuiltSection.TAG
		SECTION_MATERIALS  = dat1lib.types.sections.model.unknowns.ModelMaterialSection.TAG

		#

		materials_section = model.dat1.get_section(SECTION_MATERIALS)
		materials = materials_section.triples
		for i, q in enumerate(materials):
			mat_aid = "{:016X}".format(q[0])
			matfile = model.dat1.get_string(materials_section.string_offsets[i][0])
			matname = model.dat1.get_string(materials_section.string_offsets[i][1])			
			result["materials"] += [{
				"name": matname,
				"file": matfile,
				"aid": mat_aid
			}]

		#

		looks_section = model.dat1.get_section(SECTION_LOOK)
		looks_built_section = model.dat1.get_section(SECTION_LOOK_BUILT)

		looks = looks_section.looks
		looks_built = looks_built_section.looks

		# determine non-empty LODs
		for i in range(8):
			empty = True
			for look in looks:
				if look.lods[i].count > 0:
					empty = False
					break

			if not empty:
				result["lods"] += [i]

		#

		for i in range(len(looks)):
			look = looks[i]
			look_built = looks_built[i]

			name = model.dat1.get_string(look_built.string_offset)
			lods = [(l.start, l.count) for l in look.lods]

			result["looks"] += [{
				"name": name,
				"lods": lods
			}]

		return result
