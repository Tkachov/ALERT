KNOWN_SECTIONS = {}

class Section(object):
	TAG = 0x0
	TYPE = 'unknown'

	def __init__(self, data):
		self._raw = data

	def save(self):
		return self._raw
