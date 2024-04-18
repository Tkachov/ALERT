# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

from server.api_utils import get_field, make_post_json_route

import dat1lib
import dat1lib.types.config
import dat1lib.types.sections.config.serialized
import dat1lib.crc32 as crc32
import dat1lib.crc64 as crc64
import dat1lib.utils as utils
import io
import os
import os.path
import re
import struct
import zipfile

def is_pathlike(s):
	return (s is not None and "." in s and ("/" in s or "\\" in s))

class StagesSuitExporter(object):
	def __init__(self, stages):
		self.stages = stages

	#

	def boot(self):
		path = ".cache/.temp/"
		os.makedirs(path, exist_ok=True)
		for fn in os.listdir(path):
			full_fn = os.path.join(path, fn)
			try:
				os.remove(full_fn)
			except:
				pass

	#

	def get_exported_suit(self, filename):
		filename = filename.replace("/", "").replace("\\", "")
		full_fn = os.path.join(".cache/.temp/", filename)
		if os.path.isfile(full_fn):
			return open(full_fn, "rb")
		raise Exception("Not found")

	def make_export_suit(self, stage):
		result = {"models": [], "textures": []}

		stage_object, _ = self.stages.get_stage(stage)
		found_assets = self.scan_for_assets(stage_object, stage, {"textures": [0x5C4580B9], "models": [0x98906B9F, 0xDB40514C]})

		for locator, model in found_assets["models"]:
			details = "Model"
			if model.MAGIC == 0x98906B9F:
				details = "MSMR Model"
			elif model.MAGIC == 0xDB40514C:
				details = "MM Model"

			result["models"] += [{"locator": locator, "details": details}]

		for locator, texture in found_assets["textures"]:
			w, h = 0, 0
			try:
				s = texture.dat1.get_section(0x4EDE3593)
				w, h = s.sd_width, s.sd_height
				if s.hd_mipmaps > 0:
					w, h = s.hd_width, s.hd_height
			except:
				pass
			
			result["textures"] += [{"locator": locator, "width": w, "height": h}]

		return result

	def scan_for_assets(self, stage_object, stage_name, needles):
		results = {}
		needle_magics = set()
		for k in needles:
			results[k] = []
			for m in needles[k]:
				needle_magics.add(m)

		for aid in stage_object.aid_to_path:
			path = stage_object.aid_to_path[aid]
			for s in stage_object.spans:
				full_fn = os.path.join(stage_object.path, s, path)
				if not os.path.isfile(full_fn):
					continue

				magic = self.get_file_magic(full_fn)
				if magic is None or magic not in needle_magics:
					continue

				locator = "{}/{}/{}".format(stage_name, s, path)
				_, asset = self.stages.state.get_asset(locator)
				if asset is None:
					continue

				for k in needles:
					if magic in needles[k]:
						results[k] += [(locator, asset)]

		return results

	def get_file_magic(self, fn):
		magic = None

		try:
			f = open(fn, "rb")
			magic = f.read(4)
			f.close()
		except:
			pass

		try:
			return struct.unpack("<I", magic)[0]
		except:
			pass

		return None

	#

	def export_suit(self, form):
		stage = get_field(form, "stage")
		stage_object, _ = self.stages.get_stage(stage, create_if_needed=False)
		if stage_object is None:
			raise Exception("Bad stage")

		#

		suit_id = get_field(form, "suit_id")
		if suit_id is None or suit_id == "":
			raise Exception("Bad ID")

		#

		model = get_field(form, "model")		
		if model is None or model == "":
			raise Exception("Bad .model")

		_, asset = self.stages.state.get_asset(model)
		if asset is None:
			raise Exception("Bad .model")

		#

		suit_name = get_field(form, "suit_name")

		#

		game = get_field(form, "game")
		if game == "msmr":
			icon = get_field(form, "msmr_icon")
			return self._export_msmr_suit(stage, stage_object, suit_id, suit_name, model, asset, icon)

		elif game == "mm":
			thumb_icon = get_field(form, "mm_thumb_icon")
			chest_icon = get_field(form, "mm_chest_icon")
			return self._export_mm_suit(stage, stage_object, suit_id, suit_name, model, asset, thumb_icon, chest_icon)

		raise Exception("Unsupported target game")

	def _export_msmr_suit(self, stage, stage_object, suit_id, suit_name, model, asset, icon):
		assets_to_pack = [] # (span, aid, type="locator"|"data", locator, data, override_magic=None|int)
		renaming_map = {} # aid => aid

		#

		new_model_name = "characters/hero/hero_{0}/hero_{0}.model".format(suit_id)
		new_model_aid = "{:016X}".format(crc64.hash(new_model_name))

		model = self.stages.state.locator(model)
		renaming_map[model.asset_id] = new_model_aid

		#

		assets_to_pack += self._make_configs("msmr", suit_id, new_model_name)

		assets_to_pack += [(0, new_model_aid, "locator", model, None, 0x98906B9F)] # TODO: constant for model types all over the place

		def get_variants(stage, stage_object, aid):
			if aid not in stage_object.aid_to_path:
				return []
			return stage_object.get_asset_variants_locators(stage, aid)

		refs = self.stages.state.references.get_references(model, 100)
		for d, ref in refs:
			staged_variants = get_variants(stage, stage_object, ref.aid)
			for l in staged_variants:
				l = self.stages.state.locator(l)
				override_magic = None
				magic = self.get_file_magic(l.path)
				if magic is not None:
					if magic == 0x18757E9C: # material
						override_magic = 0x1C04EF8C
					elif magic == 0xFF60342A: # materialtemplate
						override_magic = 0x07DC03E3
				assets_to_pack += [(int(l.span), l.asset_id, "locator", l, None, override_magic)] # TODO: normal span_name=>span_index conversion

		# TODO: automatic material/texture renaming
		# TODO: option to include non-staged references (so MSMR materials/textures could be brought to MM easily)
		# TODO: refactor the code, so MSMR/MM routes are not copy-pasted

		#

		self._add_icon(suit_id, icon, renaming_map, assets_to_pack)

		#

		files_to_zip = {} # "filename" => BytesIO

		id_txt = io.BytesIO()
		id_txt.write(suit_id.encode('ascii'))
		id_txt.seek(0)
		files_to_zip["{}/id.txt".format(suit_id)] = id_txt

		if suit_name is not None and suit_name != "":
			name_txt = io.BytesIO()
			name_txt.write(suit_name.encode('ascii'))
			name_txt.seek(0)
			files_to_zip["{}/name.txt".format(suit_id)] = name_txt

		archive = io.BytesIO()

		info_txt = io.BytesIO()
		# info_txt.write(bytearray([1])) # -- for MM

		offset = 0
		common_type = 0x00002744 # have no idea what are these bytes
		for pack_asset_info in assets_to_pack:
			span, aid, pack_type, locator, data, override_magic = pack_asset_info			
			sz = 0

			if pack_type == "locator":
				data = self.stages.state.get_asset_data(locator)
			elif pack_type == "data":
				data = data.read()

			sz = len(data)
			if override_magic is None:
				archive.write(data)
			else:
				write_from = 0

				if sz >= 4:
					archive.write(struct.pack("<I", override_magic))
					write_from = 4

				if sz >= 44:
					archive.write(data[write_from:40])
					archive.write(struct.pack("<I", override_magic))
					write_from = 44

				archive.write(data[write_from:])

			info_txt.write(struct.pack("<IIIQB", offset, common_type, sz, int(aid, 16), span))
			offset += sz

		info_txt.write(bytearray([0]))

		archive.seek(0)
		info_txt.seek(0)
		files_to_zip["{0}/{0}".format(suit_id)] = archive
		files_to_zip["{}/info.txt".format(suit_id)] = info_txt

		#

		filename = '{}.suit'.format(suit_id)
		fullname = ".cache/.temp/" + filename

		with zipfile.ZipFile(fullname, 'w', zipfile.ZIP_DEFLATED) as zf:
			for fn in files_to_zip:
				zf.writestr(fn, files_to_zip[fn].read())

		return {"download": filename}

	def _make_configs(self, target_game, suit_id, model_path):
		assets_to_pack = [self._make_inventory_config(suit_id)]
		assets_to_pack += [self._make_equipment_config(suit_id)]
		assets_to_pack += [self._make_itemloadout_config(target_game, suit_id)]
		assets_to_pack += [self._make_vanity_config(target_game, suit_id, model_path)]
		return assets_to_pack

	def _make_inventory_config(self, suit_id):
		filename = "configs/inventory/inv_reward_loadout_{}.config".format(suit_id)
		aid = "{:016X}".format(crc64.hash(filename))

		type_json = {"Type": "LoadoutRewardConfig"}
		content_json = {
			"ItemLoadoutConfig": {
				"AssetPath": "configs/masteritemloadoutlist/itemloadout_spiderman_{}.config".format(suit_id),
				"Autoload": False
			},
			"Name": suit_id,
			"Stackable": False
		}

		f = self._make_config(type_json, content_json, [])

		return (0, aid, "data", None, f, None)

	def _make_equipment_config(self, suit_id):
		filename = "configs/equipment/equip_techweb_suit_{}.config".format(suit_id)
		aid = "{:016X}".format(crc64.hash(filename))

		type_json = {"Type": "TechItemConfig"}
		content_json = {"Name": "Classic Suit Item"}

		f = self._make_config(type_json, content_json, [])

		return (0, aid, "data", None, f, None)

	def _make_itemloadout_config(self, target_game, suit_id):
		filename = "configs/masteritemloadoutlist/itemloadout_spiderman_{}.config".format(suit_id)
		aid = "{:016X}".format(crc64.hash(filename))

		body_type = "configs/VanityBodyType/VanityBody_SpiderMan.config"
		vanity_hed = "configs/VanityHED/VanityHEDSpiderMan1.config"
		vanity_tor1 = "configs/VanityTOR1/vanity_spiderman_{}.config".format(suit_id)
		default_vanity = "configs/vanitytor1/vanity_spiderman_classic.config" # doubt this is actually needed

		if target_game == "mm":
			body_type = "configs/VanityBodyType/VanityBody_MilesMorales.config"
			default_vanity = "configs/vanitytor1/vanity_spiderman_miles_classic_suit.config"			

		type_json = {"Type": "ItemLoadoutConfig"}
		content_json = {
			"Loadout": {
				"ItemLoadoutLists": {
					"Items": [
						{"Item": body_type},
						{"Item": vanity_hed},
						{"Item": vanity_tor1}
					]
				},
				"Name": suit_id
			}
		}
		references = [
			body_type,
			vanity_hed,
			default_vanity,
			vanity_tor1
		]

		f = self._make_config(type_json, content_json, references)

		return (0, aid, "data", None, f, None)

	def _make_vanity_config(self, target_game, suit_id, model_path):
		filename = "configs/vanitytor1/vanity_spiderman_{}.config".format(suit_id)
		aid = "{:016X}".format(crc64.hash(filename))

		name = "Spider-Man Classic"
		if target_game == "mm":
			name = "Miles Classic Suit"

		type_json = {"Type": "VanityItemConfig"}
		content_json = {
			"ModelList": {
				"Model": {
					"AssetPath": model_path,
					"Autoload": False
				},
				"BodyType": "kAll"
			},
			"ShaderUpdater": {
				"Type": "SkinShaderUpdaterPrius"
			},
			"PartType": "kTypeBareTorsoAndArms",
			"Name": name,
			"Category": "kDefaultItem",
			"Available": "kDefault"
		}

		f = self._make_config(type_json, content_json, [])

		return (0, aid, "data", None, f, None)

	def _make_config(self, type_json, content_json, references):
		config = dat1lib.types.config.Config.make()
		config.dat1.add_section_obj(dat1lib.types.sections.config.serialized.ConfigTypeSection.make(type_json, [], config.dat1))
		config.dat1.add_section_obj(dat1lib.types.sections.config.serialized.ConfigContentSection.make(content_json, [], config.dat1))

		if len(references) > 0:
			ref_section = dat1lib.types.sections.config.references.ReferencesSection.make(config.dat1)
			config.dat1.add_section_obj(ref_section)

			for r in references:
				r = r.replace("/", "\\")
				aid = crc64.hash(r)
				_, ext = os.path.splitext(r)
				ext_c32 = crc32.hash(ext)
				ref_section.entries += [(aid, config.dat1.add_string(r), ext_c32)]

		f = io.BytesIO()
		config.save(f)
		f.seek(0)
		return f

	def _export_mm_suit(self, stage, stage_object, suit_id, suit_name, model, asset, thumb_icon, chest_icon):
		assets_to_pack = [] # (span, aid, type="locator"|"data", locator, data, override_magic=None|int)
		renaming_map = {} # aid => aid

		#

		new_model_name = "characters/hero/hero_{0}/hero_{0}.model".format(suit_id)
		new_model_aid = "{:016X}".format(crc64.hash(new_model_name))

		model = self.stages.state.locator(model)
		renaming_map[model.asset_id] = new_model_aid

		#

		assets_to_pack += self._make_configs("mm", suit_id, new_model_name)

		assets_to_pack += [(0, new_model_aid, "locator", model, None, 0xDB40514C)] # TODO: constant for model types all over the place

		def get_variants(stage, stage_object, aid):
			if aid not in stage_object.aid_to_path:
				return []
			return stage_object.get_asset_variants_locators(stage, aid)

		refs = self.stages.state.references.get_references(model, 100)
		for d, ref in refs:
			staged_variants = get_variants(stage, stage_object, ref.aid)
			for l in staged_variants:
				l = self.stages.state.locator(l)
				override_magic = None
				magic = self.get_file_magic(l.path)
				if magic is not None:
					if magic == 0x1C04EF8C: # material
						override_magic = 0x18757E9C
					elif magic == 0x07DC03E3: # materialtemplate
						override_magic = 0xFF60342A
				assets_to_pack += [(int(l.span), l.asset_id, "locator", l, None, override_magic)] # TODO: normal span_name=>span_index conversion

		# TODO: automatic material/texture renaming

		#

		self._add_icon(suit_id, thumb_icon, renaming_map, assets_to_pack)
		self._add_icon(suit_id, chest_icon, renaming_map, assets_to_pack)

		#

		files_to_zip = {} # "filename" => BytesIO

		id_txt = io.BytesIO()
		id_txt.write(suit_id.encode('ascii'))
		id_txt.seek(0)
		files_to_zip["{}/id.txt".format(suit_id)] = id_txt

		if suit_name is not None and suit_name != "":
			name_txt = io.BytesIO()
			name_txt.write(suit_name.encode('ascii'))
			name_txt.seek(0)
			files_to_zip["{}/name.txt".format(suit_id)] = name_txt

		archive = io.BytesIO()

		info_txt = io.BytesIO()
		info_txt.write(bytearray([1]))

		offset = 0
		common_type = 0x00002744 # have no idea what are these bytes
		for pack_asset_info in assets_to_pack:
			span, aid, pack_type, locator, data, override_magic = pack_asset_info			
			sz = 0

			if pack_type == "locator":
				data = self.stages.state.get_asset_data(locator)
			elif pack_type == "data":
				data = data.read()

			sz = len(data)
			if override_magic is None:
				archive.write(data)
			else:
				write_from = 0

				if sz >= 4:
					archive.write(struct.pack("<I", override_magic))
					write_from = 4

				if sz >= 44:
					archive.write(data[write_from:40])
					archive.write(struct.pack("<I", override_magic))
					write_from = 44

				archive.write(data[write_from:])

			info_txt.write(struct.pack("<IIIQB", offset, common_type, sz, int(aid, 16), span))
			offset += sz

		info_txt.write(bytearray([0]))

		archive.seek(0)
		info_txt.seek(0)
		files_to_zip["{0}/{0}".format(suit_id)] = archive
		files_to_zip["{}/info.txt".format(suit_id)] = info_txt

		#

		filename = '{}.suit'.format(suit_id)
		fullname = ".cache/.temp/" + filename

		with zipfile.ZipFile(fullname, 'w', zipfile.ZIP_DEFLATED) as zf:
			for fn in files_to_zip:
				zf.writestr(fn, files_to_zip[fn].read())

		return {"download": filename}

	def _add_icon(self, suit_id, icon, renaming_map, assets_to_pack):
		if icon is not None and icon != "":
			new_icon_name = "ui/textures/pause/character/suit_{}.texture".format(suit_id)
			new_icon_aid = "{:016X}".format(crc64.hash(new_icon_name))

			icon = self.stages.state.locator(icon)
			renaming_map[icon.asset_id] = new_icon_aid

			assets_to_pack += [(0, new_icon_aid, "locator", icon, None, None)]
