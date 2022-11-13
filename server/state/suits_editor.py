import flask
from server.api_utils import get_field, make_get_json_route, make_post_json_route

import dat1lib.types.sections.config.serialized
import dat1lib.types.sections.config.references
import dat1lib.crc64 as crc64
import io
import os
import os.path
import struct
import zipfile

#

BLANK_PIC = bytes.fromhex("89504E470D0A1A0A0000000D49484452000000120000000D01030000009E80AC5A00000003504C5445F2F2F264038A6B0000000B4944415408D76320030000003400019232F3470000000049454E44AE426082")

CONFIG_CONTENT_TAG = dat1lib.types.sections.config.serialized.ConfigContentSection.TAG
CONFIG_REFERENCES_TAG = dat1lib.types.sections.config.references.ReferencesSection.TAG

SYSTEM_PROGRESSION_CONFIG_AID     = 0x9C9C72A303FCFA30 # configs/system/system_progression.config
MASTERITEMLOADOUTLIST_CONFIG_AID  = 0x9550E5741C2C7114 # configs/masteritemloadoutlist/masteritemloadoutlist.config
VANITYMASTERLIST_CONFIG_AID       = 0x9CEADD22304ADD84 # configs/vanitymasterlist/vanitymasterlist.config
VANITYMASTERLISTLAUNCH_CONFIG_AID = 0x939887A999564798 # configs/vanitymasterlist/vanitymasterlistlaunch.config

#

import dat1lib.types.toc
import dat1lib.types.sections.toc.archives
import dat1lib.types.sections.toc.asset_ids
import dat1lib.types.sections.toc.mod0
import dat1lib.types.sections.toc.offsets
import dat1lib.types.sections.toc.sizes
import dat1lib.types.sections.toc.spans

SECTION_ARCHIVES_MAP = dat1lib.types.sections.toc.archives.ArchivesSection.TAG
SECTION_ASSET_IDS = dat1lib.types.sections.toc.asset_ids.AssetIdsSection.TAG
SECTION_OFFSET_ENTRIES = dat1lib.types.sections.toc.offsets.OffsetsSection.TAG
SECTION_SIZE_ENTRIES = dat1lib.types.sections.toc.sizes.SizesSection.TAG
SECTION_SPAN_ENTRIES = dat1lib.types.sections.toc.spans.SpansSection.TAG

def new_archive(toc, fn):
	s = toc.dat1.get_section(SECTION_ARCHIVES_MAP)
	for i, a in enumerate(s.archives):
		ndx = len(a.filename)
		for j in range(len(a.filename)):
			if a.filename[j] == 0:
				ndx = j
				break

		arch_fn = a.filename[:ndx].decode('ascii')
		print(repr(arch_fn), repr(fn), arch_fn == fn)
		if arch_fn == fn:
			return i

	s.archives += [dat1lib.types.sections.toc.archives.ArchiveFileEntry.make(0, 10000 + len(s.archives), fn)]
	toc.dat1.refresh_section_data(SECTION_ARCHIVES_MAP)
	return len(s.archives)-1

def add_or_reroute_asset(toc, asset_id, archive_offset, asset_size, archive_index, span_to_append_to, fail_if_not_found=False):
	assets = toc.dat1.get_section(SECTION_ASSET_IDS)
	sizes = toc.dat1.get_section(SECTION_SIZE_ENTRIES)
	offsets = toc.dat1.get_section(SECTION_OFFSET_ENTRIES)

	def find_asset_index(needle): # linear search =\
		for i, aid in enumerate(assets.ids):
			if aid == needle:
				return i
		return -1

	asset_index = find_asset_index(asset_id) # TODO: search within specified span?
	if asset_index == -1:
		if fail_if_not_found:
			raise Exception("Asset {:016X} not found".format(asset_id))

		spans = toc.dat1.get_section(SECTION_SPAN_ENTRIES)
		span = spans.entries[span_to_append_to]
		asset_index = span.asset_index + span.count

		spans.entries[span_to_append_to].count += 1
		for i in range(span_to_append_to+1, len(spans.entries)):
			spans.entries[i].asset_index += 1

		assets.ids = assets.ids[:asset_index] + [asset_id] + assets.ids[asset_index:]
		sizes.entries = sizes.entries[:asset_index] + [dat1lib.types.sections.toc.sizes.SizeEntry(struct.pack("<III", 1, 0, asset_index))] + sizes.entries[asset_index:] # updated lower
		offsets.entries = offsets.entries[:asset_index] + [dat1lib.types.sections.toc.offsets.OffsetEntry(struct.pack("<II", 0, 0))] + offsets.entries[asset_index:] # updated lower

		toc.dat1.refresh_section_data(SECTION_SPAN_ENTRIES)
		toc.dat1.refresh_section_data(SECTION_ASSET_IDS)

	sizes.entries[asset_index].value = asset_size
	offsets.entries[asset_index].archive_index = archive_index
	offsets.entries[asset_index].offset = archive_offset

	toc.dat1.refresh_section_data(SECTION_SIZE_ENTRIES)
	toc.dat1.refresh_section_data(SECTION_OFFSET_ENTRIES)

def reroute_asset(toc, asset_id, archive_offset, asset_size, archive_index):
	add_or_reroute_asset(toc, asset_id, archive_offset, asset_size, archive_index, 0, True)

def sort_assets(toc):
	assets = toc.dat1.get_section(SECTION_ASSET_IDS)
	sizes = toc.dat1.get_section(SECTION_SIZE_ENTRIES)
	offsets = toc.dat1.get_section(SECTION_OFFSET_ENTRIES)
	spans = toc.dat1.get_section(SECTION_SPAN_ENTRIES)

	for span in spans.entries:
		span_range = range(span.asset_index, span.asset_index + span.count)

		vals = [(assets.ids[i], sizes.entries[i], offsets.entries[i]) for i in span_range]
		vals = sorted(vals, key=lambda x: x[0])

		for i in span_range:
			v = vals[i - span.asset_index]
			assets.ids[i] = v[0]
			sizes.entries[i] = v[1]
			offsets.entries[i] = v[2]

	for i in range(len(assets.ids)):
		sizes.entries[i].index = i

	toc.dat1.refresh_section_data(SECTION_SIZE_ENTRIES)
	toc.dat1.refresh_section_data(SECTION_OFFSET_ENTRIES)
	toc.dat1.refresh_section_data(SECTION_ASSET_IDS)

#

class SuitsEditor(object):
	def __init__(self, state):
		self.state = state

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/suits_editor/make", self.make_editor)
		make_post_json_route(app, "/api/suits_editor/refresh_icons", self.refresh_icons)
		make_post_json_route(app, "/api/suits_editor/install_suit", self.install_suit)
		make_get_json_route(app, "/api/suits_editor/icon", self.get_icon, False)

	def make_editor(self):
		return self.get_suits_editor()

	def refresh_icons(self):
		return self.cache_icons()

	def install_suit(self):
		rq = flask.request
		suit = rq.files["suit"].read()
		return self._install_suit(io.BytesIO(suit))

	def get_icon(self):
		aid = get_field(flask.request.args, "aid")
		return self.get_cached_icon_png(aid)

	# internal

	def boot(self):
		os.makedirs(".cache/suits/", exist_ok=True)

	#

	def _get_config(self, aid):
		toc = self.state.toc_loader.toc
		entry = toc.get_asset_entries_by_assetid(aid, True)
		data, asset = self.state._read_asset(entry[0].index)
		return asset

	def _get_progression_config(self):
		return self._get_config(SYSTEM_PROGRESSION_CONFIG_AID)

	def get_suits_editor(self):
		result = {
			"suits": [],
			"references": []
		}

		asset = self._get_progression_config()
		s = asset.dat1.get_section(CONFIG_CONTENT_TAG)
		j = s.root
		for techlist in j["TechWebLists"]:
			if "Description" not in techlist or techlist["Description"] != "Suits":
				continue

			result["suits"] = techlist["TechWebItems"]
			break

		s = asset.dat1.get_section(CONFIG_REFERENCES_TAG)
		if s is not None:
			result["references"] = [("{:016X}".format(x[0]), asset.dat1.get_string(x[1])) for x in s.entries]

		return result

	#

	def _get_cached_icon_path(self, aid, index):
		return ".cache/suits/{}.{:08X}.png".format(aid, self.state.thumbnails._get_asset_metahash(index))

	def get_cached_icon_png(self, aid):
		node = self.state.toc_loader._get_node_by_aid(aid)
		aid, variants = node[0], node[1]
		for index, archive_index in variants:
			fn = self._get_cached_icon_path(aid, index)
			if os.path.exists(fn):
				f = open(fn, "rb")
				return (flask.send_file(f, mimetype='image/png', max_age=0), 200)

		return (flask.send_file(io.BytesIO(BLANK_PIC), mimetype='image/png', max_age=0), 200)

	#

	def _normalize_path(self, path):
		return path.lower().replace('\\', '/')

	def cache_icons(self):
		editor = self.get_suits_editor()
		result = {}

		references_map = {}
		for aid, path in editor["references"]:
			references_map[self._normalize_path(path)] = aid

		for s in editor["suits"]:
			if "PreviewImage" in s:
				aid = references_map[self._normalize_path(s["PreviewImage"])]
				result[aid] = self._cache_icon(aid)

		return {"icons": result}

	def _cache_icon(self, aid):
		node = self.state.toc_loader._get_node_by_aid(aid)
		aid, variants = node[0], node[1]

		for index, archive_index in variants:
			if self._try_caching_icon(aid, index):
				return True

		return False

	def _try_caching_icon(self, aid, index):
		try:
			fn = self._get_cached_icon_path(aid, index)
			data, asset = self.state._get_asset_by_index(index)

			if isinstance(asset, dat1lib.types.autogen.Texture):
				img = self.state.textures._load_dds_mipmap(asset, None, 0)
				if img is None:
					return False

				img.save(fn)
				return True
		except:
			print(traceback.format_exc())

		return False

	#

	def _install_suit(self, suit):
		zf = zipfile.ZipFile(suit)

		id_fn = None
		files_dir = None
		for n in zf.namelist():
			if os.path.basename(n) == "id.txt":
				id_fn = n
				files_dir = os.path.dirname(n)

		suitname = zf.read(id_fn).decode("ascii")
		info = zf.read(files_dir + "/info.txt")
		container = zf.read(files_dir + "/" + suitname)

		#

		progression = self._get_progression_config()
		loadout_list = self._get_config(MASTERITEMLOADOUTLIST_CONFIG_AID)
		vanity_list = self._get_config(VANITYMASTERLIST_CONFIG_AID)
		vanity_list_launch = self._get_config(VANITYMASTERLISTLAUNCH_CONFIG_AID)

		self._mod_progression(progression, suitname)
		self._mod_loadout_list(loadout_list, suitname)
		# base3 and base4 are the unmodded for some reason

		os.makedirs(os.path.join(self.state.toc_loader.toc._archives_dir, "Suits"), exist_ok=True)
		self._reroute_asset_via_new_archive(SYSTEM_PROGRESSION_CONFIG_AID, progression, "Suits\\base1")
		self._reroute_asset_via_new_archive(MASTERITEMLOADOUTLIST_CONFIG_AID, loadout_list, "Suits\\base2")
		self._reroute_asset_via_new_archive(VANITYMASTERLIST_CONFIG_AID, vanity_list, "Suits\\base3")
		self._reroute_asset_via_new_archive(VANITYMASTERLISTLAUNCH_CONFIG_AID, vanity_list_launch, "Suits\\base4")

		#

		suit_archive = "Suits\\" + suitname
		suit_archive_fn = os.path.join(self.state.toc_loader.toc._archives_dir, suit_archive)
		with open(suit_archive_fn, "wb") as f:
			f.write(container)

		#

		toc = self.state.toc_loader.toc
		archive_index = new_archive(toc, suit_archive)

		SIZE = 21
		count = len(info) // SIZE
		entries = [struct.unpack("<IIIQB", info[i*SIZE:(i+1)*SIZE]) for i in range(count)]

		for e in entries:
			off, _, sz, aid, span_to_append_to = e
			add_or_reroute_asset(toc, aid, off, sz, archive_index, span_to_append_to)
			# TODO: update toc_loader's internals as well

		sort_assets(toc)

		#

		with open(self.state.toc_loader.toc_path, "wb") as f:
			toc.save(f)

		self.state.toc_loader.reboot() # TODO: update toc_loader's internals instead of requiring reload

		return {}

	def _mod_progression(self, progression, suitname):
		reward_reference = "configs\\inventory\\inv_reward_loadout_{}.config".format(suitname)
		icon_reference = "ui\\textures\\pause\\character\\suit_{}.texture".format(suitname)
		equip_reference = "configs\\equipment\\equip_techweb_suit_{}.config".format(suitname)

		reward_normalized = self._normalize_path(reward_reference)
		icon_normalized = self._normalize_path(icon_reference)
		equip_normalized = self._normalize_path(equip_reference)

		reward_aid = crc64.hash(reward_normalized)
		icon_aid = crc64.hash(icon_normalized)
		equip_aid = crc64.hash(equip_normalized)

		s = progression.dat1.get_section(CONFIG_CONTENT_TAG)
		j = s.root

		# Suits list

		suits_techlist = None
		for techlist in j["TechWebLists"]:
			if "Description" not in techlist or techlist["Description"] != "Suits":
				continue

			suits_techlist = techlist["TechWebItems"]
			break

		if suits_techlist is None:
			raise Exception("'Suits' not found in system_progression.config!")

		found = False
		needle = "SUIT_{}".format(suitname)
		for s in suits_techlist:
			if "Name" in s and s["Name"] == needle:
				found = True

		if not found:
			suits_techlist += [{
				"GivesItems": {
					"Item": reward_normalized
				},
				"SkillItem": equip_normalized,
				"UnhideByItem": equip_normalized,
				"PreviewImage": icon_normalized,
				"DisplayName": "CHARWEB_MAY",
				"Description": "CHARWEB_MAY_TITLE",
				"Icon": "icon_tech_web_suit",
				"Name": needle
			}]

		# UnlockForFree

		uff = j["UnlockForFree"]
		if needle not in uff:
			uff += [needle]

		# references

		s = progression.dat1.get_section(CONFIG_REFERENCES_TAG)
		if s is None:
			raise Exception("References section not found in system_progression.config!")

		s.print_verbose({}) # TODO
		print("adding ", reward_aid, 0xA9F149C4, reward_reference)
		print("adding ", icon_aid, 0x95A3A227, icon_reference)
		print("adding ", equip_aid, 0xA9F149C4, equip_reference)

		self._add_reference(progression.dat1, s, reward_aid, 0xA9F149C4, reward_reference)
		self._add_reference(progression.dat1, s, icon_aid, 0x95A3A227, icon_reference)
		self._add_reference(progression.dat1, s, equip_aid, 0xA9F149C4, equip_reference)

		s.print_verbose({}) # TODO

		progression.dat1.refresh_section_data(CONFIG_CONTENT_TAG)
		progression.dat1.refresh_section_data(CONFIG_REFERENCES_TAG)
		progression.dat1.recalculate_section_headers()

	def _mod_loadout_list(self, loadout_list, suitname):
		config_reference = "configs\\masteritemloadoutlist\\itemloadout_spiderman_{}.config".format(suitname)
		config_normalized = self._normalize_path(config_reference)
		config_aid = crc64.hash(config_normalized)

		s = loadout_list.dat1.get_section(CONFIG_CONTENT_TAG)
		j = s.root

		# ItemLoadoutConfigs

		vanity_category_list = None
		for category_list in j["ItemLoadoutCategoryList"]:
			if "Category" not in category_list or category_list["Category"] != "kVanity":
				continue

			vanity_category_list = category_list["ItemLoadoutConfigs"]
			break

		if vanity_category_list is None:
			raise Exception("'kVanity' category not found in masteritemloadoutlist.config!")

		if config_normalized not in vanity_category_list:
			vanity_category_list += [config_normalized]

		# references

		s = loadout_list.dat1.get_section(CONFIG_REFERENCES_TAG)
		if s is None:
			raise Exception("References section not found in masteritemloadoutlist.config!")

		s.print_verbose({}) # TODO
		print("adding ", config_aid, 0xA9F149C4, config_reference)

		self._add_reference(loadout_list.dat1, s, config_aid, 0xA9F149C4, config_reference)

		s.print_verbose({}) # TODO

		loadout_list.dat1.refresh_section_data(CONFIG_CONTENT_TAG)
		loadout_list.dat1.refresh_section_data(CONFIG_REFERENCES_TAG)
		loadout_list.dat1.recalculate_section_headers()

	def _add_reference(self, dat1, section, aid, ext_c32, path):
		found = False
		for e in section.entries:
			if e[0] == aid:
				found = True
				break

		if not found:
			section.entries += [(aid, dat1.add_string(path), ext_c32)]

	def _reroute_asset_via_new_archive(self, aid, asset, archive_name):
		# save file

		asset_size = None
		full_fn = os.path.join(self.state.toc_loader.toc._archives_dir, archive_name)
		with open(full_fn, "wb") as f:
			asset.save(f)
			asset_size = f.tell()

		# add (or update) toc's archive entry & asset entry

		toc = self.state.toc_loader.toc
		archive_index = new_archive(toc, archive_name)
		
		reroute_asset(toc, aid, 0, asset_size, archive_index)

		# TODO: update toc_loader's internals as well
