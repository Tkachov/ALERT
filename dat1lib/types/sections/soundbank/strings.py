# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections

class StringsSection(dat1lib.types.sections.Section):
	TAG = 0x3E8490A3 # Sound Bank Strings

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# asset original filename, and all Wwise object names ordered by FNV hash value

		self._strings = []
		self._strings_map = {}

		offset = 0
		start = 0
		while offset < len(data):
			if data[offset] == 0 or offset == len(data)-1:
				end = offset-1
				if data[offset] == 0:
					end = offset

				s = data[start:end].decode("utf-8")
				self._strings += [s]
				self._strings_map[start] = s

				offset += 1
				r = offset % 4
				if r > 0:
					offset += 4-r

				start = offset
				continue

			offset += 1

	def get_string(self, offset):
		return self._strings_map.get(offset, None)

	def get_string_by_index(self, ndx):
		if ndx < 0 or ndx >= len(self._strings):
			return None

		return self._strings[ndx]

	def get_strings(self):
		return self._strings
