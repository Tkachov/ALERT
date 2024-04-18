# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib
import dat1lib.crc32 as crc32
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
		map_scaling = 1.0
		map_offset_x = 0.0
		map_offset_y = 0.0

		params = {}
		textures = {}

		if material is not None:
			# material template

			template_path = material.dat1.get_string(0x44)
			if material.dat1.version == dat1lib.VERSION_SO:
				template_path = material.dat1.get_string(0x54)
			if template_path is not None:
				mtm_aid = "{:016X}".format(crc64.hash(template_path))
				if material.dat1.version == dat1lib.VERSION_SO:
					mtm_aid = "{:016X}".format(crc32.hash(template_path))
				template = find_asset_by_aid(state, stage, mtm_aid)
				if template is not None:
					section = template.dat1.get_section(0x1CAFE804)
					if section is not None:
						for i in range(len(section.entries)):
							spos, _, _, slot, _ = section.entries[i]
							s = template.dat1.get_string(spos)
							textures[slot] = s

					params_keys = None
					params_values = None

					section = template.dat1.get_section(0x45C4F4C0)
					if section is not None:
						params_keys = section.params_keys

					section = template.dat1.get_section(0xA59F667B)
					if section is not None:
						params_values = section.data

					if params_keys is not None and params_values is not None:
						for offset, size, key in params_keys:
							params[key] = params_values[offset:offset+size]

			# material overrides

			section = material.dat1.get_section(0xB967FF7A)
			if section is not None:
				for i in range(len(section.entries)):
					spos, _, _, slot, _ = section.entries[i]
					s = material.dat1.get_string(spos)
					textures[slot] = s

			section = material.dat1.get_section(0xF5260180)
			if section is not None:
				for k, v in section.params:
					params[k] = v

				for texture in section.textures:
					spos, shash = texture
					filename = section._get_string(spos)
					textures[shash] = filename

			section = material.dat1.get_section(0xD9B12454)
			if section is not None:
				filename = material.dat1.get_string(section.texture_c)
				if filename is not None:
					textures[0xABDAD780] = filename

				filename = material.dat1.get_string(section.texture_n)
				if filename is not None:
					textures[0x7AE34E7A] = filename


		map_prefix = ""
		for k in params:
			v = params[k]
			if v is None:
				continue

			if k == 0x4BAAD667: # DiffuseColor
				R, G, B = struct.unpack("<3f", v)

			elif k == 0x24F4CA4C: # Glossiness
				struct.unpack("<f", v)[0]

			elif k == 0x01876E44:
				map_scaling = struct.unpack("<f", v)[0]

			elif k == 0x15FA754B:
				map_offset_y = map_offset_x = 1.0 / struct.unpack("<f", v)[0]

			elif k == 0x7F058428:
				maps["Kd"] = "{} {} {}".format(*struct.unpack("<3f", v))

		map_prefix = "-s {} {} {} ".format(map_scaling, map_scaling, map_scaling)
		map_prefix += "-o {} {} {} ".format(map_offset_x, map_offset_y, 0)

		#

		for k in textures:
			filename = textures[k]
			if filename is None:
				continue

			tex_aid = "{:016X}".format(crc64.hash(filename))
			if material.dat1.version == dat1lib.VERSION_SO:
				tex_aid = "{:016X}".format(crc32.hash(filename))
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

			if k == 0xABDAD780 or k == 0x2EE380F1 or k == 0x2E475254: # BaseMap2D_Texture; ?; ?
				maps["map_Kd"] = map_prefix + url
				if "Kd" in maps:
					del maps["Kd"]

			if k == 0x7AE34E7A or k == 0xCAAA9AB5: # NormalMap2D_Texture; ?
				maps["norm"] = map_prefix + url

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
		if materials_section is None:
			return

		if materials_section.version == dat1lib.VERSION_SO:
			materials = materials_section.string_offsets
			for i, q in enumerate(materials):
				matfile = model.dat1.get_string(q[0])
				matname = model.dat1.get_string(q[1])
				mat_aid = "{:016X}".format(0)
				if matfile is not None:
					mat_aid = "{:016X}".format(crc32.hash(matfile))
				self.write_material(matname, stage, mat_aid, state)
		else:
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
