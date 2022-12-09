import os.path
import time

# TODO: make these configurable
MAX_CACHED_DATA_SIZE = 256 * 1024 * 1024
MAX_CACHED_ENTRIES = 100

DEBUG = False
def log(x):
	if DEBUG:
		print(x)

class CacheEntry(object):
	def __init__(self, data):
		self.data = bytearray()
		self.data[:] = data
		self.timestamp = int(time.time())

	def get(self):
		self.timestamp = int(time.time())
		return self.data

class DataCache(object):
	def __init__(self, caches):
		self.caches = caches
		self.cached = {}
		self.cache_size = 0

	#

	def clear(self):
		self.cached = {}
		self.cache_size = 0

	def get(self, locator):
		log("DataCache.get: {}".format(locator))
		state = self.caches.state
		locator = state.locator(locator)

		# don't cache non-archived asset data

		if not locator.is_valid:
			raise Exception("Invalid Locator passed: {}".format(locator))

		if not locator.is_archived:
			log("\tcache miss: not archived")

			path = os.path.join("stages/", locator.path)
			if not os.path.exists(path):
				path = os.path.join("stages/", locator.stage, locator.span, locator.asset_id)

			f = open(path, "rb")
			data = f.read()
			f.close()

			return data

		# return asset data if it is cached

		key = self._get_cache_key(locator)
		if key in self.cached:
			log("\tcache hit!")
			return self.cached[key].get()

		# extract data from toc

		log("\tcache miss, loading...")

		toc = state.toc_loader.toc
		i = state._get_archived_asset_index(locator)

		try:
			data = toc.extract_asset(i)
			self._cache(key, data)
			return self.cached[key].get()
		except Exception as e:
			error_msg = "{}".format(e)

			if "Errno 2" in error_msg and "No such file or directory" in error_msg:
				ri = len(error_msg)-1
				while ri >= 0:
					if error_msg[ri] == '/' or error_msg[ri] == '\\':
						break
					ri -= 1

				raise Exception("missing archive '{}".format(error_msg[ri+1:]))

			raise

	#

	def _get_cache_key(self, locator):
		return str(locator)

	def _cache_limits_exceeded(self):
		return (len(self.cached) > MAX_CACHED_ENTRIES or self.cache_size > MAX_CACHED_DATA_SIZE)

	def _cache(self, key, data):
		self.cached[key] = CacheEntry(data)
		self.cache_size += len(data)
		log("\t-- added {}, now {} entries of {} size".format(key, len(self.cached), self.cache_size))

		if self._cache_limits_exceeded():
			log("\t-- limits exceeded: {}/{} entries of {}/{} size".format(len(self.cached), MAX_CACHED_ENTRIES, self.cache_size, MAX_CACHED_DATA_SIZE))
			keys = sorted([(self.cached[k].timestamp, k) for k in self.cached]) # first key is the earliest used (least needed right now)

			for ts, k in keys:
				if k == key: # can't uncache an entry we just created, even if limits are exceeded
					continue

				if not self._cache_limits_exceeded():
					break

				if k in self.cached:
					entry = self.cached[k]
					self.cache_size -= len(entry.data)
					del self.cached[k]
					log("\t-- removed {}, now {} entries of {} size".format(k, len(self.cached), self.cache_size))
