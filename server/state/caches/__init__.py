from server.state.caches.data import DataCache

class Caches(object):
	def __init__(self, state):
		self.state = state
		self.data_cache = DataCache(self)

	#

	def reboot(self):
		self.data_cache.clear()

	def get_data(self, locator):
		return self.data_cache.get(locator)

	# internal

	def boot(self):
		pass
