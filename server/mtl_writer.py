import dat1lib
import dat1lib.crc64 as crc64
import dat1lib.types.model
import dat1lib.types.sections.model.geo
import dat1lib.types.sections.model.meshes
import dat1lib.types.sections.model.unknowns
import dat1lib.utils as utils
import io
import random
import struct

SECTION_INDEXES   = dat1lib.types.sections.model.geo.IndexesSection.TAG
SECTION_VERTEXES  = dat1lib.types.sections.model.geo.VertexesSection.TAG
SECTION_MESHES    = dat1lib.types.sections.model.meshes.MeshesSection.TAG
SECTION_MATERIALS = dat1lib.types.sections.model.unknowns.ModelMaterialSection.TAG

###

def get_material_name(index, dat1, materials_section):
	material_formatted = "material{:02}".format(index)
	
	matname = dat1.get_string(materials_section.string_offsets[index][1])
	if matname is not None:
		material_formatted = matname

	return material_formatted

def get_best_asset_locator(state, stage, aid):
	locator = None
	
	try:
		variants = state.get_asset_variants_locators(stage, aid)
		if len(variants) > 0:
			locator = variants[0]
	except:
		pass

	try:
		if locator is None and stage is not None and stage != "":
			variants = state.get_asset_variants_locators("", aid)
			if len(variants) > 0:
				locator = variants[0]
	except:
		pass

	return locator

def find_asset_by_aid(state, stage, aid):
	locator = get_best_asset_locator(state, stage, aid)

	if locator is None:
		return None

	_, asset = state.get_asset(locator)
	return asset

###

class MtlHelper(object):
	def __init__(self):
		self.f = io.BytesIO(bytes())

	#

	def write(self, s):
		self.f.write(s.encode('ascii'))

	def write_material(self, matname, stage, mat_aid, state):
		self.write("newmtl {}\n".format(matname))

		#

		material = find_asset_by_aid(state, stage, mat_aid)

		#

		R, G, B = 1.0, 0.0, 0.0
		maps = {}
		random_suffix = str(random.randint(0, 10**10))

		if material is not None:
			section = material.dat1.get_section(0xF5260180)
			if section is not None:
				for k, v in section.params:
					if k == 0x4BAAD667: # DiffuseColor
						R, G, B = struct.unpack("<3f", v)

					elif k == 0x24F4CA4C: # Glossiness
						struct.unpack("<f", v)[0]

				#

				for texture in section.textures:
					spos, shash = texture
					filename = section._get_string(spos)

					if filename is None:
						continue

					tex_aid = "{:016X}".format(crc64.hash(filename))
					locator = get_best_asset_locator(state, stage, tex_aid)

					if locator is None:
						continue

					locator = state.locator(locator)
					url = "api/textures_viewer/mipmap?locator={}&mipmap_index=0#".format(locator) + random_suffix

					# TODO: other MTLLoader supported ones:
					"""				
					case 'map_ks': // Specular map

					case 'map_ke': // Emissive map

					case 'norm': // normal map

					case 'map_bump':
					case 'bump': // Bump texture map

					case 'map_d': // Alpha map
					"""

					if shash == 0xABDAD780 or shash == 0x2EE380F1: # BaseMap2D_Texture; ?
						maps["map_Kd"] = url

					if shash == 0x7AE34E7A or shash == 0xCAAA9AB5: # NormalMap2D_Texture; ?
						maps["norm"] = url					

		if len(maps) == 0:
			self.write("Kd {} {} {}\n".format(R, G, B))
		else:
			for k in maps:
				self.write("{} {}\n".format(k, maps[k]))

	def get_output(self):
		self.f.seek(0)
		return self.f

	#

	def write_materials(self, model, stage, state):
		materials_section = model.dat1.get_section(SECTION_MATERIALS)
		materials = materials_section.triples

		for i, q in enumerate(materials):
			matname = get_material_name(i, model.dat1, materials_section)

			mat_aid = "{:016X}".format(q[0])
			matfile = model.dat1.get_string(materials_section.string_offsets[i][0])
			if matfile is not None:
				mat_aid = "{:016X}".format(crc64.hash(matfile))

			self.write_material(matname, stage, mat_aid, state)

###

def write(model, stage, state):
	if stage is None:
		stage = ""

	helper = MtlHelper()
	helper.write_materials(model, stage, state)
	return helper.get_output()
