# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.crc32 as crc32
import dat1lib.types.sections
import dat1lib.types.sections.soundbank.strings
import dat1lib.utils as utils
import io
import struct

class Event(object):
	def __init__(self, data):
		self.ulid, self.small, self.flags, self.zero, self.flags2, self.a, self.b = struct.unpack("<IHHHHHH", data)
		# a == b most of the time (if not, a < b)

class InfoSection(dat1lib.types.sections.Section):
	TAG = 0x0E19E37F # Sound Bank Info
	TYPE = 'soundbank'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# SO
		# 1436 occurrences in 1473 files
		# size = 16..58672 (avg = 2086.6)
		#
		# examples: 0A39177E (min size), 91C12D8E (max size)

		# MSMR
		# 1309 occurrences in 1345 files
		# size = 16..123424 (avg = 1184.0)
		#
		# examples: 81456C2A07996ED7 (min size), 826509A0F509A671 (max size)

		# MM
		# 1164 occurrences in 1239 files
		# size = 16..97584 (avg = 841.9)
		#
		# examples: 805A011970FE88E3 (min size), AA47C17532AF52AC (max size)

		# RCRA
		# 1168 occurrences in 1218 files
		# size = 16..45792 (avg = 563.5)
		#
		# examples: 8019125F734A3957 (min size), 8E7F2FAFC675D9EF (max size)

		ENTRY_SIZE = 16
		count = len(data)//ENTRY_SIZE
		self.events = [Event(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def get_short_suffix(self):
		return "info ({} elements)".format(len(self.events))

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

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Info         | {:6} elements".format(self.TAG, len(self.events)))
		print("")
		
		table = self._make_table()
		table = table.split("\n")
		table = [(" "*9 + s) for s in table]
		table = "\n".join(table)
		print(table)

	def web_repr(self):
		content = f"{len(self.events)} elements\n\n"
		content += self._make_table()
		return {"name": "Info", "type": "text", "readonly": True, "content": content}
