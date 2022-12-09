from server.state.caches.assets import AssetsCache
from server.state.caches.data import DataCache

class Caches(object):
	def __init__(self, state):
		self.state = state
		self.assets_cache = AssetsCache(self)
		self.data_cache = DataCache(self)

	#

	def reboot(self):
		self.data_cache.clear()

	def get_data(self, locator):
		return self.data_cache.get(locator)

	def get_asset(self, locator):
		return self.assets_cache.get(locator)

	# internal

	def boot(self):
		pass
