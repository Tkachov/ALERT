# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import ctypes
import os
import os.path
import struct
import platform

lib = None
if platform.system() == "Windows":
	try:
		lib = ctypes.windll.LoadLibrary(os.path.join(os.getcwd(), "libdeflate.dll"))
	except:
		pass

kGDeflateId = 4
kDefaultTileSize = 64 * 1024

class Page(ctypes.Structure):
	_fields_ = [("data", ctypes.c_char_p), ("nbytes", ctypes.c_uint)]

def decompress_tile(compressedTile, decompressor):
	page = Page(compressedTile, len(compressedTile))
	output = bytes(kDefaultTileSize)
	actualRead = 0

	res = lib.libdeflate_gdeflate_decompress(decompressor, ctypes.pointer(page), 1, ctypes.c_char_p(output), 65536, actualRead)
	if res != 0:
		raise Exception("libdeflate error: {}".format(res))
	
	return output

def decompress(compressed, outputSize):
	output = bytearray(outputSize)
	offset = 0

	try:
		libid, magic, numTiles, _ = struct.unpack("<BBHI", compressed[offset:offset + 8])
		offset += 8

		if libid != kGDeflateId or libid ^ magic != 0xFF:
			print("bad header")
			return output

		if lib is None:
			return output

		lib.libdeflate_alloc_gdeflate_decompressor.restype = ctypes.POINTER(ctypes.c_char)
		ptr = lib.libdeflate_alloc_gdeflate_decompressor()

		tileOffsets = list(struct.unpack("<{}I".format(numTiles), compressed[offset:offset + 4 * numTiles]))
		offset += 4 * numTiles

		result = bytearray()
		for tileIndex in range(numTiles):
			tileOffset = 0
			if tileIndex > 0:
				tileOffset = tileOffsets[tileIndex]

			sz = tileOffsets[0]
			if tileIndex < numTiles - 1:
				sz = tileOffsets[tileIndex + 1] - tileOffset

			compressedTile = compressed[offset:offset + sz]
			offset += sz
			tile = decompress_tile(compressedTile, ptr)

			outputOffset = tileIndex * kDefaultTileSize
			end = min(kDefaultTileSize, outputSize - outputOffset)
			for i in range(end):
				output[outputOffset + i] = tile[i]

		lib.libdeflate_free_gdeflate_decompressor(ptr)
	except:
		pass

	return output
