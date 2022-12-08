import struct

def read_struct(f, fmt):
	sz = struct.calcsize(fmt)
	return struct.unpack(fmt, f.read(sz))

def read_struct_N_array(f, N, struct_fmt):
	return [read_struct(f, struct_fmt)[0] for i in range(N)]

def read_class_N_array(f, N, struct_class):
	return [struct_class(f) for i in range(N)]

def read_struct_array(f, size_fmt, struct_fmt):
	return read_struct_N_array(f, read_struct(f, size_fmt)[0], struct_fmt)

def read_class_array(f, size_fmt, struct_class):
	return read_class_N_array(f, read_struct(f, size_fmt)[0], struct_class)

def read_struct_N_array_data(data, N, fmt):
	sz = struct.calcsize(fmt)
	return [struct.unpack(fmt, data[i*sz:(i+1)*sz])[0] for i in range(N)]

def read_struct_array_data(data, fmt):
	sz = struct.calcsize(fmt)
	N = len(data) // sz
	return [struct.unpack(fmt, data[i*sz:(i+1)*sz]) for i in range(N)]

def read_class_array_data(data, sz, struct_class):
	N = len(data) // sz
	return [struct_class(data[i*sz:(i+1)*sz]) for i in range(N)]

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
			print(s)
			s = ""
			cnt = 0
	if s != "":
		print(s)

def format_bytes(bytes_arr):
	return " ".join(["{:02X}".format(x) for x in bytes_arr])

def treat_as_bytes(num_bytes, strct):
	bts = struct.unpack("<" + ("B" * num_bytes), strct)
	return format_bytes(bts)

def print_bytes_formatted(bytes_arr, prefix="", columns=4, bytes_per_column=4):
	N = len(bytes_arr)
	i = 0
	while i < N:
		line = prefix
		for j in range(columns):
			if i >= N:
				break

			line += format_bytes(bytes_arr[i:i+bytes_per_column])
			line += "  "
			i += bytes_per_column
		print(line)

###

def normalize_path(path):
	return path.lower().replace('\\', '/')
