import sys
import math
import traceback

EPS = 0.0001

COMPARE_BONES = True
COMPARE_MESHES = True
COMPARE_POSITIONS = True
COMPARE_NORMALS = True
COMPARE_WEIGHTS = True
COMPARE_UVS = True

BONE_POSITIONS_EPS = EPS
BONE_ROTATIONS_EPS = EPS
POSITIONS_EPS = EPS
NORMALS_EPS = EPS
WEIGHTS_EPS = EPS
UVS_EPS = EPS

def read_ascii(fn):
	f = open(fn)
	d = f.read()
	f.close()

	lines = d.split("\n")
	result = {}

	ptr = 0
	bones = int(lines[ptr])
	ptr += 1

	result["bones"] = []

	for i in range(bones):
		name = lines[ptr]
		ptr += 1
		parent = int(lines[ptr])
		ptr += 1
		xyzq = lines[ptr]
		ptr += 1

		parts = xyzq.split(" ")
		result["bones"] += [(name, parent, (float(parts[0]), float(parts[1]), float(parts[2])), (float(parts[3]), float(parts[4]), float(parts[5]), float(parts[6])))]

	#

	result["meshes"] = []

	meshes = int(lines[ptr])
	ptr += 1

	has_bones = (len(result["bones"]) > 0)

	for i in range(meshes):
		name = lines[ptr]
		ptr += 1
		uv_layers = int(lines[ptr])
		ptr += 1
		textures = int(lines[ptr])
		ptr += 1
		
		if uv_layers != 1 or textures != 0:
			print(f"mesh#{i}: unsupported uv_layers={uv_layers} or textures={textures} value!")

		vertexes_count = int(lines[ptr])
		ptr += 1

		vertexes = []
		for j in range(vertexes_count):
			position = lines[ptr].split(" ")
			ptr += 1

			normal = lines[ptr].split(" ")
			ptr += 1

			color = lines[ptr].split(" ")
			ptr += 1

			uv = lines[ptr].split(" ")
			ptr += 1

			groups = []
			weights = []
			if has_bones:
				groups = lines[ptr].split(" ")
				ptr += 1

				weights = lines[ptr].split(" ")
				ptr += 1

			vertexes += [
				(
					(float(position[0]), float(position[1]), float(position[2])),
					(float(normal[0]), float(normal[1]), float(normal[2])),
					color,
					(float(uv[0]), float(uv[1])),
					[int(x) for x in groups],
					[float(x) for x in weights]
				)
			]

		faces_count = int(lines[ptr])
		ptr += 1

		faces = []
		for j in range(faces_count):
			faces += [lines[ptr]]
			ptr += 1

		result["meshes"] += [(name, uv_layers, textures, vertexes, faces)]

	return result

###

def difference(a, b):
	r = []
	while len(r) < len(a):
		r += [0]
	for i, (a, b) in enumerate(zip(a, b)):
		r[i] = a - b
	return tuple(r)

def vector_len(a):
	r = 0
	for x in a:
		r += x*x
	return math.sqrt(r)

#

def compare_attribute(m1, m2, attr):
	print(f"# {attr}")

	if m1 == m2:
		print(f"same object passed -- {attr} are the same")
		return True

	if m1 is None:
		print(f"m1 is None -- {attr} are different")
		return False

	if m2 is None:
		print(f"m2 is None -- {attr} are different")
		return False

	m1_has_bones = (attr in m1)
	m2_has_bones = (attr in m2)

	if m1_has_bones != m2_has_bones:
		if m1_has_bones:
			print(f"m1 have {attr}, m2 doesn't have {attr} -- {attr} are different")
		else:
			print(f"m1 doesn't have {attr}, m2 have {attr} -- {attr} are different")
		return False

	if not m1_has_bones and not m2_has_bones:
		print(f"no {attr} in either m1 or m2 -- {attr} are the same")
		return False

	return True

#

def compare_bones(m1, m2):
	if not COMPARE_BONES:
		return True

	if not compare_attribute(m1, m2, "bones"):
		return False

	b1 = m1["bones"]
	b2 = m2["bones"]

	if len(b1) != len(b2):
		print(f"m1 has {len(b1)} bones, m2 has {len(b2)} bones -- bones are different")
		return False

	res = True
	for i, (a, b) in enumerate(zip(b1, b2)):
		a_name, a_parent, a_xyz, a_q = a
		b_name, b_parent, b_xyz, b_q = b

		if a_name != b_name:
			print(f"bone #{i}: name differs: {a_name} vs {b_name}")
			res = False

		if a_parent != b_parent:
			print(f"bone #{i}: parent differs: {a_parent} vs {b_parent}")
			res = False

		if a_xyz != b_xyz:
			dff = difference(a_xyz, b_xyz) # (a_xyz[0] - b_xyz[0], a_xyz[1] - b_xyz[1], a_xyz[2] - b_xyz[2])
			dfl = vector_len(dff)

			if dfl >= BONE_POSITIONS_EPS:
				print(f"bone #{i}: position differs: {a_xyz} vs {b_xyz}, diff = {dff} (len = {dfl:.6f})")
				res = False

		if a_q != b_q:
			dff = difference(a_q, b_q)
			dfl = vector_len(dff)

			if dfl >= BONE_ROTATIONS_EPS:
				print(f"bone #{i}: rotation differs: {a_q} vs {b_q}, diff = {dff} (len = {dfl:.6f})")
				res = False

	return res

#

def compare_mesh(index, m1, m2):
	res = True
	name1, uv1, tex1, verts1, faces1 = m1
	name2, uv2, tex2, verts2, faces2 = m2

	if name1 != name2:
		print(f"mesh #{index}: name differs: {name1} vs {name2}")
		res = False

	if uv1 != uv2:
		print(f"mesh #{index}: uv_layers differs: {uv1} vs {uv2}")
		res = False

	if tex1 != tex2:
		print(f"mesh #{index}: textures differs: {tex1} vs {tex2}")
		res = False

	if len(verts1) != len(verts2):
		print(f"mesh #{index}: vertexes count differs: {len(verts1)} vs {len(verts2)}")
		res = False
	else:
		for i, (a, b) in enumerate(zip(verts1, verts2)):
			a_xyz, a_normal, a_color, a_uv, a_groups, a_weights = a
			b_xyz, b_normal, b_color, b_uv, b_groups, b_weights = b

			# position

			if COMPARE_POSITIONS:
				dff = difference(a_xyz, b_xyz)
				dfl = vector_len(dff)

				if dfl >= POSITIONS_EPS:
					print(f"mesh#{index}: vertex #{i}: position differs: {a_xyz} vs {b_xyz}, diff = {dff} (len = {dfl:.6f})")
					res = False

			# normals

			if COMPARE_NORMALS:
				dff = difference(a_normal, b_normal)
				dfl = vector_len(dff)

				if dfl >= NORMALS_EPS:
					print(f"mesh#{index}: vertex #{i}: normal differs: {a_normal} vs {b_normal}, diff = {dff} (len = {dfl:.6f})")
					res = False

			# ignoring colors

			# uv

			if COMPARE_UVS:
				dff = difference(a_uv, b_uv)
				dfl = vector_len(dff)

				if dfl >= UVS_EPS:
					print(f"mesh#{index}: vertex #{i}: UV differs: {a_uv} vs {b_uv}, diff = {dff} (len = {dfl:.6f})")
					res = False

			# groups

			if COMPARE_WEIGHTS:
				if len(a_groups) != len(b_groups):
					print(f"mesh#{index}: vertex #{i}: groups count differs: {len(a_groups)} vs {len(b_groups)}")
					res = False
				else:
					diff = False
					reason = ""
					for ag, aw, bg, bw in zip(a_groups, a_weights, b_groups, b_weights):
						if ag != bg:
							diff = True
							reason = f"{ag} != {bg}"
							break
						if math.fabs(aw - bw) >= WEIGHTS_EPS:
							diff = True
							reason = f"{aw} != {bw}"
							break
					if diff:
						print(f"mesh#{index}: vertex #{i}: groups/weights differ: {reason}\n\t{a_groups}\n\t{a_weights}\n\tvs\n\t{b_groups}\n\t{b_weights}")
						res = False

	return res


def compare_meshes(m1, m2):
	if not COMPARE_MESHES:
		return True

	if not compare_attribute(m1, m2, "meshes"):
		return False

	meshes1 = m1["meshes"]
	meshes2 = m2["meshes"]

	if len(meshes1) != len(meshes2):
		print(f"m1 has {len(meshes1)} meshes, m2 has {len(meshes2)} meshes -- meshes are different")
		return False

	res = True
	for i, (a, b) in enumerate(zip(meshes1, meshes2)):
		r = compare_mesh(i, a, b)
		res = (res and r)
	return res

#

def compare(m1, m2):
	r1 = compare_bones(m1, m2)
	r2 = compare_meshes(m1, m2)
	return (r1 and r2)

###

def main(argv):
	if len(argv) < 3:
		print("Usage:")
		print(f"$ {argv[0]} <filename1> <filename2>")
		sys.exit(2)

	try:
		fn1 = argv[1]
		fn2 = argv[2]

		m1 = read_ascii(fn1)
		m2 = read_ascii(fn2)

		is_the_same = compare(m1, m2)
		res = int(not is_the_same)
		sys.exit(res)
	except Exception as e:
		traceback.print_exc()
		sys.exit(3)

if __name__ == "__main__":
	main(sys.argv)
