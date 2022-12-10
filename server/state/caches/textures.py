import dat1lib.types.sections.texture.header
import os
import os.path
import time
import threading
from PIL import Image

# TODO: make these configurable
MAX_CACHED_DATA_SIZE = 256 * 1024 * 1024
MAX_CACHED_ENTRIES = 1000

DEBUG = False
def log(x):
	if DEBUG:
		print(x)

class TexturesCache(object):
	def __init__(self, caches):
		self.caches = caches
		self.cached_entries_count = 0
		self.cache_size = 0
		self.access_timestamps = {}

		self.lock = threading.Lock()

	#

	def boot(self):
		with self.lock:
			os.makedirs(".cache/mipmaps/", exist_ok=True)
			self._update_cache_stats(init_access_timestamps=True)

	def reboot(self):
		self.boot()

	def clear(self):
		with self.lock:
			self._delete_all_cached_mipmaps()
			self._update_cache_stats(init_access_timestamps=True)

	def get(self, locator, mipmap_index, use_hd_data):
		with self.lock:
			log("TexturesCache.get: {}".format(locator))
			state = self.caches.state
			locator = state.locator(locator)

			if not locator.is_valid:
				raise Exception("Invalid Locator passed: {}".format(locator))

			#

			data, asset = state.get_asset(locator)
			info = asset.dat1.get_section(dat1lib.types.sections.texture.header.TextureHeaderSection.TAG)

			hd_data = None
			real_mipmap_index = mipmap_index
			if use_hd_data:
				if mipmap_index < info.hd_mipmaps:
					hd_locator = state._make_hd_locator(locator)
					hd_data = state.get_asset_data(hd_locator)
				else:
					mipmap_index -= info.hd_mipmaps
			else:
				real_mipmap_index += info.hd_mipmaps

			# return cached, if any

			key = self._get_cache_key(locator, real_mipmap_index)
			if os.path.exists(key):
				log("\tcache hit!")
				return self._get_cached(key)

			# if not, convert .dds to .png and cache it

			log("\tcache miss, loading...")

			saved_already, image = state.textures.dds_to_png(asset, hd_data, mipmap_index, save_as=key)

			if image is None: # failure to load
				return None

			if saved_already:
				self._cache(key, None) 
				return self._get_cached(key, image)

			self._cache(key, image)
			return self._get_cached(key)

	#

	def _get_cache_key(self, locator, mipmap_index):
		prefix = "{}{}".format("" if locator.stage is None else locator.stage, "" if locator.stage is None else "_")
		return ".cache/mipmaps/{}{}_{}.png".format(prefix, locator.asset_id, mipmap_index)

	def _get_cached(self, key, image=None):
		self.access_timestamps[key] = int(time.time())
		if image is not None:
			return image
		return Image.open(key)

	def _cache_limits_exceeded(self):
		return (self.cached_entries_count > MAX_CACHED_ENTRIES or self.cache_size > MAX_CACHED_DATA_SIZE)

	def _cache(self, key, image):
		if image is not None:
			f = open(key, "wb")
			image.save(f, format="png")
			f.close()

		self._update_cache_stats()
		log("\t-- added {}, now {} entries of {} size".format(key, self.cached_entries_count, self.cache_size))

		if self._cache_limits_exceeded():
			log("\t-- limits exceeded: {}/{} entries of {}/{} size".format(self.cached_entries_count, MAX_CACHED_ENTRIES, self.cache_size, MAX_CACHED_DATA_SIZE))
			keys = sorted([(self.access_timestamps[k], k) for k in self.access_timestamps]) # first key is the earliest used (least needed right now)

			for ts, k in keys:
				if k == key: # can't uncache an entry we just created, even if limits are exceeded
					continue

				if not self._cache_limits_exceeded():
					break

				if os.path.exists(k):
					sz = self._get_file_size(k)
					if self._delete_file(k):
						self.cache_size -= sz
						self.cached_entries_count -= 1
						log("\t-- removed {}, now {} entries of {} size".format(k, self.cached_entries_count, self.cache_size))

	#

	def _update_cache_stats(self, init_access_timestamps=False):
		self.cached_entries_count = 0
		self.cache_size = 0
		if init_access_timestamps:
			self.access_timestamps = {}
		now = int(time.time())

		path = ".cache/mipmaps/"
		for fn in os.listdir(path):
			full_fn = os.path.join(path, fn)
			if not os.path.isdir(full_fn):
				self.cached_entries_count += 1
				self.cache_size += self._get_file_size(full_fn)
				if init_access_timestamps:
					self.access_timestamps[full_fn] = now

	def _delete_all_cached_mipmaps(self):
		path = ".cache/mipmaps/"
		for fn in os.listdir(path):
			full_fn = os.path.join(path, fn)
			self._delete_file(full_fn)

	# generic file-related stuff

	def _get_file_size(self, fn):
		try:
			return os.path.getsize(fn)
		except:
			return 0

	def _delete_file(self, fn):
		try:
			os.remove(fn)
			return True
		except:
			return False
