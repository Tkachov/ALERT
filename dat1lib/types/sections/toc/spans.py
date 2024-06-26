# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import struct

class SpanEntry(object):
	def __init__(self, data):
		self.asset_index, self.count = struct.unpack("<II", data)

class SpansSection(dat1lib.types.sections.Section):
	TAG = 0xEDE8ADA9 # Archive TOC Header
	TYPE = 'toc'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self.entries = [SpanEntry(data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

	def get_short_suffix(self):
		return "spans ({})".format(len(self.entries))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Spans        | {:6} entries".format(self.TAG, len(self.entries)))

		"""
		for e in self.entries:
			print(e.asset_index, e.count)
		"""
