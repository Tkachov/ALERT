# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

from server.state.caches.assets import AssetsCache
from server.state.caches.data import DataCache
from server.state.caches.textures import TexturesCache

class Caches(object):
	def __init__(self, state):
		self.state = state
		self.assets_cache = AssetsCache(self)
		self.data_cache = DataCache(self)
		self.textures_cache = TexturesCache(self)
	
	#

	def reboot(self):
		self.assets_cache.clear()
		self.data_cache.clear()
		self.textures_cache.reboot()

	def get_data(self, locator):
		return self.data_cache.get(locator)

	def get_asset(self, locator):
		return self.assets_cache.get(locator)

	def get_texture_mipmap(self, locator, mipmap_index, use_hd_data):
		return self.textures_cache.get(locator, mipmap_index, use_hd_data)

	# internal

	def boot(self):
		self.textures_cache.boot()
