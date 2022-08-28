import dat1lib.types.sections
import io
import struct

class JointsMapSection(dat1lib.types.sections.UintUintMapSection): # aka model_joint_lookup
	TAG = 0xEE31971C
	TYPE = 'model'

	def __init__(self, data):
		dat1lib.types.sections.UintUintMapSection.__init__(self, data)

	def get_short_suffix(self):
		return "joints map ({})".format(len(self._map))

	def print_verbose(self, config):
		##### "{:08X} | ............ | {:6} ..."
		print "{:08X} | Joints Map   | {:6} joints".format(self.TAG, len(self._map))
