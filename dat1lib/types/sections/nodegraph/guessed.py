# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

#

class HeaderSection(dat1lib.types.sections.SerializedSection):
	TAG = 0xE5065650
	TYPE = 'NodeGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)

		# MM
		# 101 occurrences in 101 files (always present)
		# size = 48
		# always first
		#
		# examples: 8018B80E97DF19E1

		# RCRA
		# 60 occurrences in 60 files (always present)
		# size = 48
		# always first
		#
		# examples: 80B51B678F9F241B

	def get_short_suffix(self):
		return "header"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Header       |".format(self.tag))
		print(json.dumps(self.root, indent=4, sort_keys=True))
		if len(self.extras) > 0:
			print(" "*10, self.extras)

	def web_repr(self):
		return {"name": "Header", "type": "json", "readonly": True, "content": self.root}

#

class NodesListSection(dat1lib.types.sections.SerializedSection):
	TAG = 0xD8110E80
	TYPE = 'NodeGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)

		# MM
		# 101 occurrences in 101 files (always present)
		# size = 172..272716 (avg = 7976.0)
		#
		# examples: 8AC1B8D23B05FC2E (min size), BF53FB9507F5A7B0 (max size)

		# RCRA
		# 60 occurrences in 60 files (always present)
		# size = 124..4156 (avg = 710.4)
		#
		# examples: 80B51B678F9F241B (min size), 996CE3334BA854BE (max size)

	def get_short_suffix(self):
		return "nodes list"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Nodes List   |".format(self.tag))
		print(json.dumps(self.root, indent=4, sort_keys=True))
		if len(self.extras) > 0:
			print(" "*10, self.extras)

	def web_repr(self):
		return {"name": "Nodes List", "type": "json", "readonly": True, "content": self.root}

#

class ConnectionsSection(dat1lib.types.sections.SerializedSection):
	TAG = 0x7884E530
	TYPE = 'NodeGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)

		# MM
		# 101 occurrences in 101 files (always present)
		# size = 380..1518908 (avg = 42962.3)
		#
		# examples: 8AC1B8D23B05FC2E (min size), BF53FB9507F5A7B0 (max size)

		# RCRA
		# 60 occurrences in 60 files (always present)
		# size = 204..16748 (avg = 2380.5)
		#
		# examples: 80B51B678F9F241B (min size), 996CE3334BA854BE (max size)

	def get_short_suffix(self):
		return "connections"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Connections  |".format(self.tag))
		print(json.dumps(self.root, indent=4, sort_keys=True))
		if len(self.extras) > 0:
			print(" "*10, self.extras)

	def web_repr(self):
		return {"name": "Connections", "type": "json", "readonly": True, "content": self.root}

#

class MappingsSection(dat1lib.types.sections.SerializedSection):
	TAG = 0xA9894CDB
	TYPE = 'NodeGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)

		# MM
		# 101 occurrences in 101 files (always present)
		# size = 1008..2413192 (avg = 75653.3)
		# always last
		#
		# examples: 8AC1B8D23B05FC2E (min size), BF53FB9507F5A7B0 (max size)

		# RCRA
		# 60 occurrences in 60 files (always present)
		# size = 720..50544 (avg = 6689.6)
		#
		# examples: 80B51B678F9F241B (min size), 996CE3334BA854BE (max size)

	def get_short_suffix(self):
		return "mappings"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Mappings   |".format(self.tag))
		print(json.dumps(self.root, indent=4, sort_keys=True))
		if len(self.extras) > 0:
			print(" "*10, self.extras)

	def web_repr(self):
		return {"name": "Mappings", "type": "json", "readonly": True, "content": self.root}

#

class ReferencesSection(dat1lib.types.sections.ReferencesSection):
	TAG = 0xFBD496D6
	TYPE = 'NodeGraph'

	def __init__(self, data, container):
		dat1lib.types.sections.ReferencesSection.__init__(self, data, container)

		# MM
		# 49 occurrences in 101 files
		# size = 16..1360 (avg = 75.4)
		#
		# examples: 81ABBBF35AF930BC (min size), 80E88F9D2623201D (max size)

		# RCRA
		# 55 occurrences in 60 files
		# size = 16..1184 (avg = 54.6)
		#
		# examples: 96563DCFEFDB8201 (min size), 996CE3334BA854BE (max size)

	def get_short_suffix(self):
		return "references ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | References   | {:6} entries".format(self.TAG, len(self.entries)))
		dat1lib.types.sections.ReferencesSection.print_verbose(self, config)
