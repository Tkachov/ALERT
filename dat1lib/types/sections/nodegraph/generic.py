import dat1lib.types.sections
import io
import struct

class NodeGraphSection(dat1lib.types.sections.SerializedSection):
	TAG = -1
	TYPE = 'NodeGraph'

	def __init__(self, tag, data, container):
		dat1lib.types.sections.SerializedSection.__init__(self, data, container)
		self.tag = tag

	def get_short_suffix(self):
		return "type"

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print("{:08X} | Generic Node |".format(self.tag))
		print(json.dumps(self.root, indent=4, sort_keys=True))
		if len(self.extras) > 0:
			print(" "*10, self.extras)

	def web_repr(self):
		return {"name": "Node {:08X}".format(self.tag), "type": "json", "readonly": True, "content": self.root}
