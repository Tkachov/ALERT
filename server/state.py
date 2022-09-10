# -*- coding: utf-8 -*-

import dat1lib
import dat1lib.types.toc
import io
import os.path

class State(object):	
	def __init__(self):
		self.toc = None
		self.toc_path = None

		self.currently_extracted_asset = None
		self.currently_extracted_asset_index = None

	def load_toc(self, path):
		# TODO: toc is not None

		asset_archive_path = os.path.basename(path)
		toc_fn = path

		if os.path.isdir(path):
			asset_archive_path = path
			toc_fn = os.path.join(path, "toc")

		if self.toc_path is not None:
			if os.path.samefile(self.toc_path, toc_fn):
				# don't do anything, it's already loaded
				# TODO: parameter to force reload?
				return

			# TODO: not the same, should we "unload" it (if error happens, we'd still be working with old one, which might be confusing for user -- as if new one loaded correctly)

		#

		toc = None
		with open(toc_fn, "rb") as f:
			toc = dat1lib.read(f)		

		if toc is None:
			raise Exception("Couldn't comprehend '{}'".format(toc_fn))

		if not isinstance(toc, dat1lib.types.toc.TOC):
			raise Exception("Not a toc")
	
		#

		toc.set_archives_dir(asset_archive_path)

		self.toc = toc
		self.toc_path = toc_fn

	def extract_asset(self, index):
		# TODO: what if I want to force reload?
		if self.currently_extracted_asset_index == index:
			return self.currently_extracted_asset

		data = None

		try:
			data = self.toc.extract_asset(self.toc.get_asset_entry_by_index(index))
		except Exception as e:
			error_msg = "{}".format(e)

			if "Errno 2" in error_msg and "No such file or directory" in error_msg:
				def rindex(lst, value):
					return len(lst) - lst[::-1].index(value) - 1

				ri1 = rindex(error_msg, '/')
				ri2 = rindex(error_msg, '\\')
				if ri1 < ri2:
					ri1 = ri2

				raise Exception("missing archive '{}".format(error_msg[ri1+1:]))

			raise

		#

		d = io.BytesIO(data)
		obj = dat1lib.read(d, try_unknown=False)

		self.currently_extracted_asset = obj
		self.currently_extracted_asset_index = index

		return self.currently_extracted_asset
