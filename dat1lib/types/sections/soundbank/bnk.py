# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections

class WwiseBankSection(dat1lib.types.sections.Section):
	TAG = 0x53F25238

	def __init__(self, data, container):
		dat1lib.types.sections.Section.__init__(self, data, container)

	def replace_data(self, data):
		self._raw = data
