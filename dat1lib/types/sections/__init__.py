# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import struct

KNOWN_SECTIONS = {}

class Section(object):
	TAG = 0x0

	def __init__(self, data, container):
		self._raw = data
		self._dat1 = container

	def save(self):
		return self._raw

###

class UintUintMapSection(Section):
	def __init__(self, data, container):
		Section.__init__(self, data, container)

		ENTRY_SIZE = 8
		count = len(data)//ENTRY_SIZE
		self._entries = [struct.unpack("<II", data[i*ENTRY_SIZE:(i+1)*ENTRY_SIZE]) for i in range(count)]

		self._map = {}
		for (k, v) in self._entries:
			if k in self._map:
				print("[!] Map duplicated key: {:08X}={:08X} replaced with {:08X}={:08X}".format(k, self._map[k], k, v))

			self._map[k] = v

	# TODO: save()

###

class StringsSection(Section):
	def __init__(self, data, container):
		Section.__init__(self, data, container)

		self._strings = data.decode("utf-8").split('\x00')
		if self._strings[-1] == "":
			self._strings.pop()
		self._strings_map = {}

		offset = 0
		for s in self._strings:
			self._strings_map[offset] = s
			offset += len(s) + 1

	# TODO: save()

	def get_string(self, offset):
		return self._strings_map.get(offset, None)
