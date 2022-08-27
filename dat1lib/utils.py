import struct

def read_struct(f, fmt):
	sz = struct.calcsize(fmt)
	return struct.unpack(fmt, f.read(sz))

def read_struct_N_array(f, N, struct_fmt):
	return [read_struct(f, struct_fmt)[0] for i in xrange(N)]

def read_class_N_array(f, N, struct_class):
	return [struct_class(f) for i in xrange(N)]

def read_struct_array(f, size_fmt, struct_fmt):
	return read_struct_N_array(f, read_struct(f, size_fmt)[0], struct_fmt)

def read_class_array(f, size_fmt, struct_class):
	return read_class_N_array(f, read_struct(f, size_fmt)[0], struct_class)

###

def print_table(arr, fmt, entries_per_line):
	s = ""
	cnt = 0
	for x in arr:
		if s == "":
			s = "-"
		s += fmt.format(x)
		cnt += 1
		if cnt == entries_per_line:
			print s
			s = ""
			cnt = 0
	if s != "":
		print s

def format_bytes(bytes_arr):
	return " ".join(["{:02X}".format(x) for x in bytes_arr])

def treat_as_bytes(num_bytes, strct):
	bts = struct.unpack("<" + ("B" * num_bytes), strct)
	return format_bytes(bts)
