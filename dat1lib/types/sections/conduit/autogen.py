# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

class ConduitAssetRefsSection(dat1lib.types.sections.ReferencesSection):
	TAG = 0x2F4056CE # Conduit Asset Refs
	TYPE = 'Conduit'

	def __init__(self, data, container):
		dat1lib.types.sections.ReferencesSection.__init__(self, data, container)

		# SO
		# 575 occurrences in 3415 files
		# size = 4..380 (avg = 14.6)
		#
		# examples: 04458CBC (min size), 1F436835 (max size)

		# MSMR
		# 708 occurrences in 1234 files
		# size = 16..1728 (avg = 71.3)
		#
		# examples: 80035676415E24D6 (min size), AF207C743E768578 (max size)

		# MM
		# 601 occurrences in 1119 files
		# size = 16..2448 (avg = 91.3)
		#
		# examples: 8085D81AFD659637 (min size), AF207C743E768578 (max size)

		# RCRA
		# 1046 occurrences in 1070 files
		# size = 16..3088 (avg = 93.4)
		#
		# examples: 800ECA8DB20906EF (min size), 9C2BA85165B721C3 (max size)

	def get_short_suffix(self):
		return "Conduit Asset Refs ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | References   | {:6} entries".format(self.TAG, len(self.entries)))
		dat1lib.types.sections.ReferencesSection.print_verbose(self, config)

#

class ConduitBuiltSection(dat1lib.types.sections.SerializedSection):
	TAG = 0xCEB30E68 # Conduit Built
	TYPE = 'Conduit'

	def __init__(self, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)

		# SO
		# 879 occurrences in 3415 files (all .conduit?)
		# size = 76..255484 (avg = 7950.3)
		#
		# examples: 0AC7F086 (min size), C9A19964 (max size)

		# MSMR
		# 1234 occurrences in 1234 files (always present)
		# size = 72..522232 (avg = 13505.9)
		# always first
		#
		# examples: 93D2FB47CF888B46 (min size), AF207C743E768578 (max size)

		# MM
		# 1119 occurrences in 1119 files (always present)
		# size = 72..885844 (avg = 18136.9)
		# always first
		#
		# examples: 80372B922DE76D8F (min size), AF207C743E768578 (max size)

		# RCRA
		# 1070 occurrences in 1070 files (always present)
		# size = 72..299316 (avg = 13008.0)
		# always first
		#
		# examples: 821C237559C4B811 (min size), 872E298A3A2D59FD (max size)

	def get_short_suffix(self):
		return "built"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Built        |".format(self.TAG))
		print(json.dumps(self.root, indent=4, sort_keys=True))
		if len(self.extras) > 0:
			print(" "*10, self.extras)

	def web_repr(self):
		return {"name": "Conduit Built", "type": "json", "readonly": False, "content": self.root}
