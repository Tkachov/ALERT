# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import flask
from server.api_utils import get_field, make_get_json_route, make_post_json_route

import dat1lib.types.sections.config.serialized
import dat1lib.types.sections.config.references
import dat1lib.crc64 as crc64
import io
import os
import os.path
import shutil
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

_install_suit_log = None

def new_archive(toc, fn):
	global _install_suit_log

	s = toc.dat1.get_section(SECTION_ARCHIVES_MAP)
	for i, a in enumerate(s.archives):
		ndx = len(a.filename)
		for j in range(len(a.filename)):
			if a.filename[j] == 0:
				ndx = j
				break

		arch_fn = a.filename[:ndx].decode('ascii')
		if arch_fn == fn:
			return i

	# _install_suit_log += "- added new archive entry '{}'\n".format(fn)
	_install_suit_log += "- '{}' archive entry added\n".format(fn)
	s.archives += [dat1lib.types.sections.toc.archives.ArchiveFileEntry.make(0, 10000 + len(s.archives), fn)]
	toc.dat1.refresh_section_data(SECTION_ARCHIVES_MAP)
	return len(s.archives)-1

def add_or_reroute_asset(toc, asset_id, archive_offset, asset_size, archive_index, span_to_append_to, fail_if_not_found=False):
	global _install_suit_log

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

		# _install_suit_log += "- added asset '{:016X}'\n".format(asset_id)
		_install_suit_log += "- '{:016X}' asset added\n".format(asset_id)
	else:
		# _install_suit_log += "- updated asset '{:016X}'\n".format(asset_id)
		_install_suit_log += "- '{:016X}' asset updated\n".format(asset_id)

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
		stage = get_field(flask.request.form, "stage")
		return self.get_suits_editor(stage)

	def refresh_icons(self):
		stage = get_field(flask.request.form, "stage")
		return self.cache_icons(stage)

	def install_suit(self):
		rq = flask.request
		stage = get_field(rq.form, "stage")
		suit = rq.files["suit"].read()
		return self._install_suit(stage, io.BytesIO(suit))

	def get_icon(self):
		stage = get_field(flask.request.args, "stage")
		aid = get_field(flask.request.args, "aid")
		return self.get_cached_icon_png(stage, aid)

	# internal

	def boot(self):
		os.makedirs(".cache/suits/", exist_ok=True)

	#

	def _get_config(self, stage, aid):
		toc = self.state.toc_loader.toc
		entry = toc.get_asset_entries_by_assetid(aid, True)
		data, asset = self.state._read_asset(entry[0].index)
		return asset

	def get_suits_editor(self, stage):
		result = {
			"suits": [],
			"references": []
		}

		asset = self._get_config(stage, SYSTEM_PROGRESSION_CONFIG_AID)
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

	def _get_cached_icon_path(self, locator):
		locator = self.state.locator(locator)
		prefix = "{}{}".format("" if locator.stage is None else locator.stage, "" if locator.stage is None else "_")
		return ".cache/suits/{}{}.{:08X}.png".format(prefix, locator.asset_id, self.state.thumbnails._get_asset_metahash(locator))

	def get_cached_icon_png(self, stage, aid):
		locators = self.state.get_asset_variants_locators(stage, aid)
		print(locators)
		for l in locators:
			fn = self._get_cached_icon_path(l)
			print("\t", fn)
			if os.path.exists(fn):
				f = open(fn, "rb")
				return (flask.send_file(f, mimetype='image/png', max_age=0), 200)

		if stage != "":
			return self.get_cached_icon_png("", aid)

		return (flask.send_file(io.BytesIO(BLANK_PIC), mimetype='image/png', max_age=0), 200)

	#

	def _normalize_path(self, path):
		return path.lower().replace('\\', '/')

	def cache_icons(self, stage):
		editor = self.get_suits_editor(stage)
		result = {}

		references_map = {}
		for aid, path in editor["references"]:
			references_map[self._normalize_path(path)] = aid

		for s in editor["suits"]:
			if "PreviewImage" in s:
				aid = references_map[self._normalize_path(s["PreviewImage"])]
				result[aid] = self._cache_icon(stage, aid)

		return {"icons": result}

	def _cache_icon(self, stage, aid):
		locators = self.state.get_asset_variants_locators(stage, aid)
		for l in locators:
			if self._try_caching_icon(l):
				return True

		if stage != "":
			return self._cache_icon("", aid)

		return False

	def _try_caching_icon(self, locator):
		try:
			fn = self._get_cached_icon_path(locator)
			data, asset = self.state.get_asset(locator)

			if isinstance(asset, dat1lib.types.autogen.Texture):
				img = self.state.textures.load_mipmap_image(locator, 0, use_hd_data=False) # OK to pass locator after get_asset(), as it should be cached
				if img is None:
					return False

				img.save(fn)
				return True
		except:
			print(traceback.format_exc())

		return False

	#

	def _install_suit(self, stage, suit):
		global _install_suit_log
		_install_suit_log = ""
		zf = zipfile.ZipFile(suit)

		id_fn = None
		files_dir = None
		for n in zf.namelist():
			if os.path.basename(n) == "id.txt":
				id_fn = n
				files_dir = os.path.dirname(n)
				break

		suitname = zf.read(id_fn).decode("ascii")
		info = zf.read(files_dir + "/info.txt")
		container = zf.read(files_dir + "/" + suitname)

		#

		progression = self._get_config(stage, SYSTEM_PROGRESSION_CONFIG_AID)
		loadout_list = self._get_config(stage, MASTERITEMLOADOUTLIST_CONFIG_AID)
		vanity_list = self._get_config(stage, VANITYMASTERLIST_CONFIG_AID)
		vanity_list_launch = self._get_config(stage, VANITYMASTERLISTLAUNCH_CONFIG_AID)

		self._mod_progression(progression, suitname)
		self._mod_loadout_list(loadout_list, suitname)
		# base3 and base4 are the unmodded for some reason

		_install_suit_log += "'toc':\n"

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

		toc_fn = self.state.toc_loader.toc_path
		toc_bak_fn = toc_fn + ".BAK"
		if not os.path.exists(toc_bak_fn):
			shutil.copyfile(toc_fn, toc_bak_fn)
			_install_suit_log += "\nMade a backup of 'toc' in 'toc.BAK'.\n"

		#

		with open(self.state.toc_loader.toc_path, "wb") as f:
			toc.save(f)

		self.state.toc_loader.reboot() # TODO: update toc_loader's internals instead of requiring reload
		_install_suit_log += "\nDone. Reload required to see changes in 'toc'.\n"

		return {"log": _install_suit_log}

	def _mod_progression(self, progression, suitname):
		global _install_suit_log
		_install_suit_log += "'system_progression.config':\n"

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
			# _install_suit_log += "- added '{}' to 'Suits' list\n".format(needle)
			_install_suit_log += "- '{}' added to 'Suits'\n".format(needle)
		else:
			# _install_suit_log += "- '{}' already present in 'Suits' list\n".format(needle)
			_install_suit_log += "- '{}' already in 'Suits'\n".format(needle)

		# UnlockForFree

		uff = j["UnlockForFree"]
		if needle not in uff:
			uff += [needle]
			# _install_suit_log += "- added '{}' to 'UnlockForFree'\n".format(needle)
			_install_suit_log += "- '{}' added to 'UnlockForFree'\n".format(needle)
		else:
			# _install_suit_log += "- '{}' already present in 'UnlockForFree'\n".format(needle)
			_install_suit_log += "- '{}' already in 'UnlockForFree'\n".format(needle)

		# references

		s = progression.dat1.get_section(CONFIG_REFERENCES_TAG)
		if s is None:
			raise Exception("References section not found in system_progression.config!")

		self._add_reference(progression.dat1, s, reward_aid, 0xA9F149C4, reward_reference)
		self._add_reference(progression.dat1, s, icon_aid, 0x95A3A227, icon_reference)
		self._add_reference(progression.dat1, s, equip_aid, 0xA9F149C4, equip_reference)

		progression.dat1.refresh_section_data(CONFIG_CONTENT_TAG)
		progression.dat1.refresh_section_data(CONFIG_REFERENCES_TAG)
		progression.dat1.recalculate_section_headers()
		_install_suit_log += "\n"

	def _mod_loadout_list(self, loadout_list, suitname):
		global _install_suit_log
		_install_suit_log += "'masteritemloadoutlist.config':\n"

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
			# _install_suit_log += "- added '{}' to 'kVanity' category\n".format(config_normalized)
			_install_suit_log += "- '{:016X}' added to 'kVanity'\n".format(config_aid)
		else:
			# _install_suit_log += "- '{}' already present in 'kVanity' category\n".format(config_normalized)
			_install_suit_log += "- '{:016X}' already in 'kVanity'\n".format(config_aid)

		# references

		s = loadout_list.dat1.get_section(CONFIG_REFERENCES_TAG)
		if s is None:
			raise Exception("References section not found in masteritemloadoutlist.config!")

		self._add_reference(loadout_list.dat1, s, config_aid, 0xA9F149C4, config_reference)

		loadout_list.dat1.refresh_section_data(CONFIG_CONTENT_TAG)
		loadout_list.dat1.refresh_section_data(CONFIG_REFERENCES_TAG)
		loadout_list.dat1.recalculate_section_headers()
		_install_suit_log += "\n"

	def _add_reference(self, dat1, section, aid, ext_c32, path):
		global _install_suit_log
		found = False
		for e in section.entries:
			if e[0] == aid:
				found = True
				break

		if not found:
			section.entries += [(aid, dat1.add_string(path), ext_c32)]
			# _install_suit_log += "- added reference to '{:016X}' ('{}')\n".format(aid, path)
			_install_suit_log += "- '{:016X}' added to references\n".format(aid)
		else:
			# _install_suit_log += "- reference to '{:016X}' ('{}') already present\n".format(aid, path)
			_install_suit_log += "- '{:016X}' already in references\n".format(aid)

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
