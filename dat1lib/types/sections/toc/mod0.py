# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections
import json

class Mod0Section(dat1lib.types.sections.Section):
	TAG = 0x30444F4D
	TYPE = 'toc'

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)
		self.data = json.loads(data.decode('utf-8'))

	def __str__(self):
		return "{}".format(self.data)

	def get_short_suffix(self):
		return "MOD0 data"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | MOD0 JSON    |".format(self.TAG))
