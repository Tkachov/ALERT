# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import io
import struct

#

class xCF30405E_Section(dat1lib.types.sections.Section):
	TAG = 0xCF30405E
	TYPE = 'ZoneStatic_I16'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

		# 393 occurrences in 419 files
		# size = 118..2864604 (avg = 251998.4)
		#
		# examples: D30C7C24 (min size), 5687A013 (max size)
		pass

	def get_short_suffix(self):
		return "CF30405E ({} bytes)".format(len(self._raw))

	def print_verbose(self, config):
		if config.get("web", False):
			return
		
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | CF30405E     | {:6} bytes".format(self.TAG, len(self._raw)))

