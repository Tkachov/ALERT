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
