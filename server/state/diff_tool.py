# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import flask
from server.api_utils import get_field, make_post_json_route

import dat1lib.types.sections.model.geo

class DiffTool(object):
	IGNORED_SECTIONS = {
		dat1lib.types.sections.model.geo.IndexesSection,
		dat1lib.types.sections.model.geo.VertexesSection,
		dat1lib.types.sections.model.geo.x6B855EED_Section,
		dat1lib.types.sections.model.geo.ColorsSection
	}
	DIFFABLE_CLASSES = {
		# model
		dat1lib.types.sections.model.joints.JointDefinition,
		dat1lib.types.sections.model.locators.LocatorDefinition,
		dat1lib.types.sections.model.look.LOD,
		dat1lib.types.sections.model.look.Look,
		dat1lib.types.sections.model.look.LookBuilt,
		dat1lib.types.sections.model.meshes.MeshDefinition,
		dat1lib.types.sections.model.skin.SkinBatch,
		dat1lib.types.sections.model.unknowns.x7CA37DA0_Entry,

		# toc
		dat1lib.types.sections.toc.archives.ArchiveFileEntry,
		# dat1lib.types.sections.toc.asset_ids.Entry,
		# dat1lib.types.sections.toc.key_assets.Entry,
		dat1lib.types.sections.toc.offsets.OffsetEntry,
		dat1lib.types.sections.toc.sizes.SizeEntry,
		dat1lib.types.sections.toc.sizes.RcraSizeEntry,
		dat1lib.types.sections.toc.spans.SpanEntry
	}

	def __init__(self, state):
		self.state = state
		self._warned_about = set()

	# API

	def make_api_routes(self, app):
		make_post_json_route(app, "/api/diff_tool/diff", self.diff)

	def diff(self):
		locator1 = get_field(flask.request.form, "locator1")
		locator2 = get_field(flask.request.form, "locator2")
		return self.get_diff(locator1, locator2)

	# internal

	def get_diff(self, locator1, locator2):
		_, asset1 = self.state.get_asset(locator1)
		_, asset2 = self.state.get_asset(locator2)

		if asset1 is None or asset2 is None:
			raise Exception("Bad asset")

		self._warned_about = set()

		differences = []
		differences += self._diff_containers(asset1, asset2)
		differences += self._diff_dat1(asset1, asset2)
		return {"differences": differences}

	#

	def _diff_containers(self, a1, a2):
		result = []

		if a1.MAGIC != a2.MAGIC:
			result += [{"left": a1.__class__.__name__, "right": a2.__class__.__name__}]

		are_compatible = (issubclass(a1.__class__, a2.__class__) or issubclass(a2.__class__, a1.__class__))
		if are_compatible:
			result += self._diff_attributes("", a1, a2) # a1.__class__.__name__ + "."
		
		if len(result) > 0:
			return [{"group": "Containers", "differences": result}]

		return []

	def _diff_dat1(self, a1, a2):
		if "dat1" not in dir(a1) or "dat1" not in dir(a2):
			return []

		result = []

		common_sections, diff = self._diff_dat1_header(a1, a2)
		if len(diff) > 0:
			result += [{"group": "Header", "differences": diff}]

		for s in common_sections:
			result += self._diff_dat1_section(a1, a2, s)
		
		return result

	#

	def _diff_attributes(self, object_name, o1, o2, allowed=None): # assuming o1 and o2 have the same attributes
		result = []

		if allowed is None:
			allowed = set()

		if isinstance(allowed, list):
			allowed = set(allowed)

		for n in dir(o1):
			if n not in allowed and n.startswith("_"):
				continue

			a1 = getattr(o1, n)
			a2 = getattr(o2, n)
			
			t1 = type(a1)
			t2 = type(a2)

			if t1 not in [int, float, type(None), str, list, dict, tuple]:
				continue

			result += self._diff_attribute(object_name + n, a1, a2, t1, t2)

		return result

	def _diff_attribute(self, n, a1, a2, t1, t2):
		result = []

		v1, v2 = None, None
		one_line = True
		if t1 != t2:
			v1 = "{}".format(t1)
			v2 = "{}".format(t2)
		else:
			if a1 != a2:
				if t1 == int or t1 == float or t1 == type(None):
					v1 = "{}".format(a1)
					v2 = "{}".format(a2)

				elif t1 == str:
					one_line = False
					v1 = repr(a1)
					v2 = repr(a2)

				elif t1 == list or t1 == tuple:
					if t1 == tuple:
						a1 = list(a1)
						a2 = list(a2)

					if len(a1) != len(a2):
						v1 = "{} items".format(len(a1))
						v2 = "{} items".format(len(a2))
					else:
						v1 = None
						v2 = None
						for i in range(len(a1)):
							result += self._diff_attribute(n + "["+str(i)+"]", a1[i], a2[i], type(a1[i]), type(a2[i]))

				elif t1 == dict:
					k1 = a1.keys()
					k2 = a2.keys()
					if len(k1) != len(k2) or k1 != k2:
						v1 = "{} items".format(len(a1))
						v2 = "{} items".format(len(a2))
					else:
						v1 = None
						v2 = None
						for k in k1:
							result += self._diff_attribute(n + "[\""+k+"\"]", a1[k], a2[k], type(a1[k]), type(a2[k]))
				
				else:
					if t1 in self.DIFFABLE_CLASSES:
						result += self._diff_attributes(n + ".", a1, a2)
					else:
						if t1 not in self._warned_about:
							result += [{"message": "Can't diff '{}'".format(t1.__name__)}]
							self._warned_about.add(t1)

		if v1 is not None:
			result += [{"left": n + ": " + v1, "right": n + ": " + v2}]

		return result

	#

	def _diff_dat1_header(self, o1, o2):
		result = []

		for n in ["magic", "unk1", "size"]:
			a1 = getattr(o1.dat1.header, n)
			a2 = getattr(o2.dat1.header, n)

			if a1 == a2:
				continue
			
			result += [{"left": "{}: {}".format(n, a1), "right": "{}: {}".format(n, a2)}]

		#

		s1 = ["{:08X}".format(s.tag) for s in o1.dat1.header.sections]
		s2 = ["{:08X}".format(s.tag) for s in o2.dat1.header.sections]
		if len(s1) != len(s2):
			result += [{"left": "{} sections".format(len(s1)), "right": "{} sections".format(len(s2))}]

		s1_sz_off = {}
		s2_sz_off = {}
		for s in o1.dat1.header.sections:
			s1_sz_off["{:08X}".format(s.tag)] = (s.offset, s.size)
		for s in o2.dat1.header.sections:
			s2_sz_off["{:08X}".format(s.tag)] = (s.offset, s.size)

		common = set(s1) & set(s2)
		removed = set(s1) - set(s2)
		added = set(s2) - set(s1)
		all_sections = sorted(list(set(s1) | set(s2)))
		for s in all_sections:
			if s in removed:
				result += self._make_long_diff("{}  {:10}  {:10}".format(s, s1_sz_off[s][0], s1_sz_off[s][1]), None)

			elif s in common:
				if s1_sz_off[s][0] == s2_sz_off[s][0] and s1_sz_off[s][1] == s2_sz_off[s][1]:
					continue

				result += self._make_long_diff(
					"{}  {:10}  {:10}".format(s, s1_sz_off[s][0], s1_sz_off[s][1]),
					"{}  {:10}  {:10}".format(s, s2_sz_off[s][0], s2_sz_off[s][1])
				)

			else:
				result += self._make_long_diff(None, "{}  {:10}  {:10}".format(s, s2_sz_off[s][0], s2_sz_off[s][1]))

		return (sorted(list(common)), result)

	def _make_long_diff(self, a, b):
		"""
		msg = ""
		if a is not None and a != "":
			msg += "- {}\n".format(a)
		if b is not None and b != "":
			msg += "+ {}\n".format(b)
		return [{"message": msg}]
		"""
		return [{"left": a, "right": b}]

	#

	def _diff_dat1_section(self, a1, a2, s):
		def get_better_header(section):
			try:
				suf = section.get_short_suffix()
				i = suf.find(" (")
				if i != -1:
					suf = suf[:i]
				if suf == "{:08X}".format(section.TAG):
					return None
				return "{:08X} | {}: {}".format(section.TAG, section.TYPE, suf)
			except:
				return None

		tag = int(s, 16)
		s1 = a1.dat1.get_section(tag)
		s2 = a2.dat1.get_section(tag)
		
		# assuming it's impossible that sections with the same tag
		# were parsed into objects of different types here
		# or that this method is called on a section
		# that is missing from one of the dat1

		h = "{} | {}".format(s, s1.__class__.__name__)
		h2 = get_better_header(s1)
		if h2 is not None:
			h = h2

		result = []

		if type(s1) in self.IGNORED_SECTIONS:
			pass
		else:
			result += self._diff_attributes("", s1, s2, allowed=["_strings", "_entries"])

		if len(result) == 0:
			if "_raw" in dir(s1):
				if s1._raw != s2._raw:
					result = [{"message": "<raw data differs>"}]

		if len(result) > 0:
			return [{"group": h, "differences": result}]

		return []
