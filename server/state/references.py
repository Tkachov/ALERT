import flask
from server.api_utils import get_int, get_field, make_get_json_route, make_post_json_route

import dat1lib.crc64 as crc64
import dat1lib.types.autogen
import dat1lib.types.config
import dat1lib.types.model
import dat1lib.types.sections
import dat1lib.types.sections.model.unknowns
import dat1lib.utils as utils

class Reference(object):
	def __init__(self, aid, filename):
		self.aid = aid
		self.filename = filename
		self.referenced_in = []
		self.locators = []

	def add_reference_source(self, src):
		self.referenced_in += [src]

	def add_locator(self, locator):
		self.locators += [locator]

	def add_locators(self, locators):
		for l in locators:
			self.add_locator(l)

#

class References(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/references_viewer/make", self.make_viewer)

	def make_viewer(self):
		locator = get_field(flask.request.form, "locator")
		depth = get_int(flask.request.form, "depth")

		return {"viewer": self.get_references_viewer(locator, depth)}

	# internal

	def get_references_viewer(self, locator, depth):
		references = []

		locator = self.state.locator(locator)
		default_stage = locator.stage

		refs = self.get_references(locator, depth)
		for d, ref in refs:
			ref_in = []
			for r in ref.referenced_in:
				if r not in ref_in:
					ref_in += [r]

			if len(ref_in) > 1 and "Strings Block" in ref_in:
				ref_in.remove("Strings Block")

			best_locator = self._get_best_locator(ref.locators, default_stage)
			if best_locator is not None:
				best_locator = str(best_locator)

			references += [{
				"depth": d,
				"asset_id": ref.aid,
				"filename": ref.filename,
				"referenced_in": ref_in,
				"locator": best_locator,
				"comment": self._make_comment(ref)
			}]

		return {"references": references}

	def _make_comment(self, ref):
		if len(ref.locators) == 0:
			return "Not found"

		game = False
		stages = set()

		for l in ref.locators:
			lo = self.state.locator(l)
			if lo.stage is None:
				game = True
			else:
				stages.add(lo.stage)

		comment = "Found in "
		
		if game:
			comment += "Game Archive"

		if len(stages) > 0:
			if game:
				comment += ", "

			if len(stages) > 1:
				comment += "{} stages".format(len(stages))
			else:
				for s in stages:
					comment += s
					break

		return comment

	#

	def get_references(self, locator, depth=0):
		were_queued = set()
		order = [] # (depth:int, :Reference)

		locator = self.state.locator(locator)
		default_stage = locator.stage

		q = [(0, 0, locator, [locator.asset_id])]
		while len(q) > 0:
			append_after, current_depth, locator, parent_assets = q[0]
			q = q[1:]

			orig_append_after = append_after
			refmap = {} # aid:string => :Reference
			_, asset = self.state.get_asset(locator)
			refs = self._get_references(asset)

			for aid, filename, section in refs:
				if aid not in refmap:
					refmap[aid] = Reference(aid, filename)
					refmap[aid].add_locators(self._get_locators(aid))

				refmap[aid].add_reference_source(section)

			already_added = set()
			append_to_q = []
			for aid, _, _ in refs:
				if aid in already_added:
					continue

				order = order[:append_after] + [(current_depth, refmap[aid])] + order[append_after:]
				append_after += 1
				already_added.add(aid)

				if current_depth < depth and aid not in parent_assets:
					best_locator = self._get_best_locator(refmap[aid].locators, default_stage)
					if best_locator is not None:
						append_to_q += [(append_after, current_depth+1, best_locator, parent_assets + [aid])]

			new_q = []
			for aa, b, c, d in q:
				new_aa = aa
				if aa >= orig_append_after:
					new_aa += append_after - orig_append_after
				new_q += [(new_aa, b, c, d)]
			q = new_q
			q = append_to_q + q

		return order

	def _get_best_locator(self, locators, default_stage):
		for l in locators:
			lo = self.state.locator(l)
			if lo.stage == default_stage:
				return lo

		if len(locators) > 0:
			return locators[0]

		return None

	def _get_references(self, asset):
		result = []
		# TODO: make `get_references()` in every asset type
		result += self._get_generic_references(asset)
		result += self._get_model_references(asset)
		result += self._get_material_references(asset)
		result += self._get_materialtemplate_references(asset)
		return result

	def _get_generic_references(self, asset):
		if asset is None:
			return []

		result = []

		def is_pathlike(s):
			return (s is not None and "." in s and ("/" in s or "\\" in s))

		for s in asset.dat1._strings_inverse_map:
			if is_pathlike(s):
				aid = "{:016X}".format(crc64.hash(s))
				result += [(aid, s, "Strings Block")]

		for s in asset.dat1.sections:
			if s is None:
				continue

			if isinstance(s, dat1lib.types.sections.ReferencesSection):
				for x in s.entries:
					st = s._dat1.get_string(x[1])
					result += [("{:016X}".format(x[0]), st, "References ({:08X})".format(s.TAG))]

		return result

	def _get_model_references(self, model):
		if model is None or not isinstance(model, dat1lib.types.model.Model):
			return []

		result = []

		# materials

		SECTION_MATERIALS = dat1lib.types.sections.model.unknowns.ModelMaterialSection.TAG
		materials_section = model.dat1.get_section(SECTION_MATERIALS)
		materials = materials_section.triples

		for i, q in enumerate(materials):
			mat_aid = "{:016X}".format(q[0])
			matfile = model.dat1.get_string(materials_section.string_offsets[i][0])
			if matfile is not None:
				mat_aid = "{:016X}".format(crc64.hash(matfile))

			result += [(mat_aid, matfile, "Materials ({:08X})".format(SECTION_MATERIALS))]

		return result

	def _get_material_references(self, material):
		if material is None or not isinstance(material, dat1lib.types.material.Material):
			return []

		result = []

		# material template

		template_path = material.dat1.get_string(0x44)
		if template_path is not None:
			mtm_aid = "{:016X}".format(crc64.hash(template_path))
			result += [(mtm_aid, template_path, "Strings Block")]

		# material overrides

		section = material.dat1.get_section(0xF5260180)
		if section is not None:
			for texture in section.textures:
				spos, shash = texture
				filename = section._get_string(spos)
				aid = "{:016X}".format(crc64.hash(filename))
				result += [(aid, filename, "F5260180")]

		section = material.dat1.get_section(0xD9B12454)
		if section is not None:
			filename = material.dat1.get_string(section.texture_c)
			if filename is not None:
				aid = "{:016X}".format(crc64.hash(filename))
				result += [(aid, filename, "D9B12454")]

			filename = material.dat1.get_string(section.texture_n)
			if filename is not None:
				aid = "{:016X}".format(crc64.hash(filename))
				result += [(aid, filename, "D9B12454")]

			filename = material.dat1.get_string(section.texture_g)
			if filename is not None:
				aid = "{:016X}".format(crc64.hash(filename))
				result += [(aid, filename, "D9B12454")]

			filename = material.dat1.get_string(section.texture_c2)
			if filename is not None:
				aid = "{:016X}".format(crc64.hash(filename))
				result += [(aid, filename, "D9B12454")]

		return result

	def _get_materialtemplate_references(self, template):
		if template is None or not isinstance(template, dat1lib.types.autogen.MaterialGraph):
			return []

		result = []

		section = template.dat1.get_section(0x1CAFE804)
		if section is not None:
			for i in range(len(section.entries)):
				spos, _, _, slot, _ = section.entries[i]
				s = template.dat1.get_string(spos)
				aid = "{:016X}".format(crc64.hash(s))
				result += [(aid, s, "1CAFE804")]

		return result

	#

	def _get_locators(self, aid):
		result = []

		try:
			variants = self.state.get_asset_variants_locators("", aid)
			result += variants
		except:
			pass

		for stage in self.state.stages.stages:
			try:
				variants = self.state.get_asset_variants_locators(stage, aid)
				result += variants
			except:
				pass

		return result
