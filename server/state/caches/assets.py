# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib
import dat1lib.types.dat1
import io
import time
import threading
import zlib

from server.state.types.headless_dat1 import HeadlessDAT1

# TODO: make this configurable
MAX_CACHED_ENTRIES = 100

DEBUG = False
def log(x):
	if DEBUG:
		print(x)

class CacheEntry(object):
	def __init__(self, asset, data_crc):
		self.asset = asset
		self.crc = data_crc
		self.timestamp = int(time.time())

	def get(self):
		self.timestamp = int(time.time())
		return self.asset

class AssetsCache(object):
	def __init__(self, caches):
		self.caches = caches
		self.cached = {}

		self.lock = threading.Lock()

	#

	def clear(self):
		with self.lock:
			self.cached = {}

	def get(self, locator):
		with self.lock:
			log("AssetsCache.get: {}".format(locator))
			state = self.caches.state
			locator = state.locator(locator)

			data = state.get_asset_data(locator)
			if len(data) < 4:
				return data, None

			# return asset if it is cached

			crc = self._get_data_crc(data)
			key = self._get_cache_key(locator)
			if key in self.cached:
				if self.cached[key].crc == crc:
					log("\tcache hit!")
					return data, self.cached[key].get()
				else:
					log("\tcache miss, wrong data CRC (cached={:08X}, actual={:08X}) => reloading...".format(self.cached[key].crc, crc))
			else:
				log("\tcache miss, loading...")

			# make asset if not

			d = io.BytesIO(data)
			asset = dat1lib.read(d, try_unknown=False)

			if isinstance(asset, dat1lib.types.dat1.DAT1):
				asset = HeadlessDAT1(asset)

			self._cache(key, asset, crc)
			return data, self.cached[key].get()

	#

	def _get_data_crc(self, data):
		return zlib.crc32(data, 0)

	def _get_cache_key(self, locator):
		return str(locator)

	def _cache_limits_exceeded(self):
		return (len(self.cached) > MAX_CACHED_ENTRIES)

	def _cache(self, key, asset, crc):
		self.cached[key] = CacheEntry(asset, crc)
		log("\t-- added {}, now {} entries".format(key, len(self.cached)))

		if self._cache_limits_exceeded():
			log("\t-- limits exceeded: {}/{} entries".format(len(self.cached), MAX_CACHED_ENTRIES))
			keys = sorted([(self.cached[k].timestamp, k) for k in self.cached]) # first key is the earliest used (least needed right now)

			for ts, k in keys:
				if k == key: # can't uncache an entry we just created, even if limits are exceeded
					continue

				if not self._cache_limits_exceeded():
					break

				if k in self.cached:
					self.cached[k].asset = None
					self.cached[k] = None
					del self.cached[k]
					log("\t-- removed {}, now {} entries".format(k, len(self.cached)))
