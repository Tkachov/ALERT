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
