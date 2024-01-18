import lz4.block # pip3 install lz4
import os
import struct
import sys
import traceback

DSAR_MAGIC = 0x52415344
DSAR_VERSION = 0x10003

def main(argv):
	if len(argv) < 2:
		print("Usage:")
		print("$ {} <filename>".format(argv[0]))
		print("")
		print("If <filename> is DSAR archive, uncompress it to <filename>.dec.")
		print("Otherwise, compress it into DSAR archive to <filename>.dsar.")
		return

	fn = argv[1]
	try:
		with open(fn, "rb") as f:
			magic, = struct.unpack("<I", f.read(4))
			f.seek(0)

			if magic == DSAR_MAGIC:				
				decompress_dsar(f, fn + ".dec")
			else:
				compress_to_dsar(f, fn + ".dsar")
	except:
		print("[!] Couldn't process '{}'".format(fn))
		traceback.print_exc()
		sys.exit(1)

def decompress_dsar(f, ofn):
	with open(ofn, "wb") as of:
		magic, version, blocks_count, header_end, full_size, _ = struct.unpack("<4I2Q", f.read(32))
		blocks = []
		for i in range(blocks_count):
			real_offset, comp_offset, real_size, comp_size, compression_type = struct.unpack("<2Q2IB", f.read(32)[:25]) # rest is padding
			if compression_type != 3:
				raise Exception(f"unsupported DSAR compression type: {compression_type}")

			blocks += [(real_offset, comp_offset, real_size, comp_size)]		

		if f.tell() < header_end:
			print("warning: did not expect to read header fully and not end up on first block position")
			f.read(header_end - f.tell())

		if f.tell() > header_end:
			raise Exception(f"bad header")

		for block in blocks:
			real_offset, comp_offset, real_size, comp_size = block
			if of.tell() != real_offset:
				raise Exception("uncompressed offsets out of order or don't add up with uncompressed sizes")

			f.seek(comp_offset)
			comp_data = f.read(comp_size)

			data = lz4.block.decompress(comp_data, uncompressed_size=real_size)
			of.write(data)

def compress_to_dsar(f, ofn):
	BLOCK_SIZE = 262144

	f.seek(0, os.SEEK_END)
	orig_size = f.tell()

	blocks_count = orig_size // BLOCK_SIZE
	if orig_size % BLOCK_SIZE != 0:
		blocks_count += 1

	with open(ofn, "wb") as of:
		of.write(struct.pack("<4IQ", DSAR_MAGIC, DSAR_VERSION, blocks_count, 32 + blocks_count*32, orig_size))
		of.write(b"PADDING*")

		for i in range(blocks_count):
			of.write(struct.pack("<2Q2IB", 0, 0, 0, 0, 3))
			for j in range(7):
				of.write(b"\x55")

		f.seek(0)
		for i in range(blocks_count):
			real_offset = f.tell()
			comp_offset = of.tell()
			
			data = f.read(BLOCK_SIZE)
			real_size = len(data)

			comp_data = lz4.block.compress(data, store_size=False)
			comp_size = len(comp_data)

			jump_back_to = of.tell()
			of.seek(32 + i*32)
			of.write(struct.pack("<2Q2I", real_offset, comp_offset, real_size, comp_size))

			of.seek(jump_back_to)
			of.write(comp_data)

if __name__ == "__main__":
	main(sys.argv)
