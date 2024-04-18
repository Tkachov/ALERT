# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import io

def decompress(comp_data, real_size):
	comp_size = len(comp_data)
	real_data = [b'\0' for i in range(real_size)]
	real_data = [0 for i in range(real_size)]
	real_i = 0
	comp_i = 0

	while real_i <= real_size and comp_i < comp_size:
		# direct

		a, b = comp_data[comp_i], 0
		comp_i += 1

		if (a & 240) == 240:
			b = comp_data[comp_i]
			comp_i += 1

		direct = (a >> 4) + b
		while direct >= 270 and (direct - 15) % 255 == 0:
			v = comp_data[comp_i]
			comp_i += 1
			direct += v
			if v == 0:
				break

		for i in range(direct):
			if real_i + i >= real_size or comp_i + i >= comp_size:
				break
			real_data[real_i + i] = comp_data[comp_i + i]
		real_i += direct
		comp_i += direct

		reverse = (a & 15) + 4

		if not (real_i <= real_size and comp_i < comp_size):
			break

		# reverse

		a, b = comp_data[comp_i], comp_data[comp_i + 1]
		comp_i += 2

		reverse_offset = a + (b << 8)
		if reverse == 19:
			reverse += comp_data[comp_i]
			comp_i += 1

			while reverse >= 274 and (reverse - 19) % 255 == 0:
				v = comp_data[comp_i]
				comp_i += 1
				reverse += v
				if v == 0:
					break

		for i in range(reverse):
			try:
				real_data[real_i + i] = real_data[real_i - reverse_offset + i]
			except:
				pass
		real_i += reverse

	return bytearray(real_data)

def decompress_file(f, real_size):
	data = decompress(f.read(), real_size)
	return io.BytesIO(data)
