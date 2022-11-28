import dat1lib.crc64
import string

def is_hex(s):
	return all(c in string.hexdigits for c in s)

class Locator(object):
	def __init__(self, s):
		self.path = s
		self.is_archived = False
		self.stage = ""
		self.span = ""
		self.asset_path = ""
		self.asset_id = ""
		self.is_valid = False

		if len(s) > 0:
			if s[0] == '/':
				self.is_archived = True
				self.stage = None

				i = s.find('/', 1)
				if i != -1:
					self.span = int(s[1:i])
					self.asset_path = None
					self.asset_id = s[i+1:]
					self.is_valid = True
			else:
				i1 = s.find('/')
				i2 = s.find('/', i1+1)
				if i1 != -1 and i2 != -1:
					self.stage = s[:i1]
					self.span = s[i1+1:i2]
					self.asset_path = s[i2+1:]
					if len(self.asset_path) == 16 and is_hex(self.asset_path):
						self.asset_path = None
						self.asset_id = s[i2+1:]
					else:	
						self.asset_id = "{:016X}".format(dat1lib.crc64.hash(self.asset_path))
					self.is_valid = True

	def __str__(self):
		return self.path
