# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import os.path
import re
import zipfile

class StagesModImporter(object):
	def __init__(self, stages):
		self.stages = stages

	def import_smpcmod(self, smpcmod, stage):
		zf = zipfile.ZipFile(smpcmod)
		stage_object, _ = self.stages.get_stage(stage)
		used_spans = {}

		for n in zf.namelist():
			if "ModFiles" not in n:
				continue

			basename = os.path.basename(n)
			m = re.match("^(\\d+)_([0-9A-Fa-f]{16})$", basename)
			if not m:
				continue

			archive, aid = m.groups()
			asset_data = zf.read(n)

			if aid not in used_spans:
				used_spans[aid] = []
			span = self.import_asset(stage_object, aid, int(archive), asset_data, used_spans[aid])
			used_spans[aid] += [span]

		return {"success": True}

	def import_asset(self, stage, asset_id, archive_index, asset_data, restricted_spans):
		asset_path = self.make_asset_path(asset_id)
		span_index = self.find_span_by_archive_index(asset_id, archive_index, restricted_spans)
		stage.stage_asset_data(asset_path, span_index, asset_data)
		return span_index

	#

	def make_asset_path(self, aid):
		path = aid
		if aid in self.stages.state.toc_loader._known_paths:
			path = self.stages.state.toc_loader._known_paths[aid]
		return path

	#

	def find_span_by_archive_index(self, asset_id, archive_index, restricted_spans):
		indexes = self.find_asset_indexes(asset_id)
		local_restricted_spans = []

		for s in restricted_spans:
			local_restricted_spans += [s]

		toc = self.stages.state.toc_loader.toc
		offsets_section = toc.get_offsets_section()

		for (index, locator) in indexes:
			locator = self.stages.state.locator(locator)
			
			if offsets_section.entries[index].archive_index == archive_index:
				return locator.span

			local_restricted_spans += [locator.span]

		# if we're here, it means we couldn't find span, and we just make it up
		# but we can't use spans that we have checked, or the ones we already used on import

		span_index = 0
		while True:
			if span_index not in local_restricted_spans:
				break
			span_index += 1

		return span_index

	def find_asset_indexes(self, asset_id):
		result = []

		locators = []
		try:
			locators = self.stages.state.get_asset_variants_locators("", asset_id)
		except:
			pass

		for l in locators:
			try:
				index = self.stages.state._get_archived_asset_index(l)
				result += [(index, l)]
			except:
				pass

		return result
