# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import dat1lib.types.sections.soundbank.strings
import struct

class Event(object):
	def __init__(self, data):
		self.ulid, self.small, self.flags, self.zero, self.flags2, self.a, self.b = struct.unpack("<IHHHHHH", data)
		# a == b most of the time (if not, a < b)

class InfoSection(dat1lib.types.sections.Section):
	TAG = 0x0E19E37F # Sound Bank Info

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.events = [Event(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def _make_table(self):
		def fnv(s):
			v = 2166136261
			s = s.lower()
			for c in s:
				v = ((v * 16777619) & 0xFFFFFFFF) ^ (ord(c) & 0xFF)
			return v

		strings_section = self._dat1.get_section(dat1lib.types.sections.soundbank.strings.StringsSection.TAG)

		result = ""
		###########| 12  12345678  1234  12345  1234  12345  12345  12345
		result += "  #       ulID     ?  flags  zero  flag2      ?      ?\n"
		result += "------------------------------------------------------\n"
		for i, e in enumerate(self.events):
			s = strings_section.get_string_by_index(i+1)
			h = 0
			if s is not None:
				h = fnv(s)

			suff = ""
			if s is not None and e.ulid == h:
				suff = f"  <- '{s}'"

			result += "- {:<2}  {:08X}  {:4}  {:5}  {:4}  {:5}  {:5}  {:5}{}\n".format(i, e.ulid, e.small, e.flags, e.zero, e.flags2, e.a, e.b, suff)

		result += "\n"
		return result

	def print_info(self):
		print(f"{len(self.events)} elements\n\n")
		print(self._make_table())
