# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib.types.sections

class HeadlessSerializedSection(dat1lib.types.sections.SerializedSection):
	TAG = -1
	TYPE = 'Headless'

	def __init__(self, tag, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)
		self.tag = tag

	def get_short_suffix(self):
		return "serialized"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Serialized   |".format(self.tag))
		print(json.dumps(self.root, indent=4, sort_keys=True))
		if len(self.extras) > 0:
			print(" "*10, self.extras)

	def web_repr(self):
		return {"name": "{:08X}".format(self.tag), "type": "json", "readonly": True, "content": self.root}

class HeadlessDAT1(object):
	MAGIC = 0x44415431

	def __init__(self, dat1):
		self.magic = dat1.header.magic
		self._raw_dat1 = None

		dat1._outer = self
		self.dat1 = dat1

		for i, s in enumerate(dat1.header.sections):
			if dat1.sections[i] is not None:
				continue

			data = dat1._sections_data[i]
			if len(data) > 8 and data[:8] == b"\x00\x00\x00\x00\x44\x00\x15\x03":
				try:
					dat1.sections[i] = HeadlessSerializedSection(s.tag, data, dat1)
				except:
					pass

	def save(self, f):
		self.dat1.full_refresh()
		self.dat1.save(f)

	def print_info(self, config):
		self.dat1.print_info(config)
