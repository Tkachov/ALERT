import dat1lib.types.dat1
import io
import struct
import sys
import zlib

class DAG(object):
	MAGIC = 0x891F77AF

	def __init__(self, f):
		self.magic, self.size, self.unk1 = struct.unpack("<III", f.read(12))

		if self.magic != self.MAGIC:
			print("[!] Bad 'dag' magic: {} (isn't equal to expected {})".format(self.magic, self.MAGIC))
		
		dec = zlib.decompressobj(0)
		data = dec.decompress(f.read())

		if len(data) != self.size:
			print("[!] Actual decompressed size {} isn't equal to one written in the file {}".format(len(data), self.size))

		self.dat1 = dat1lib.types.dat1.DAT1(io.BytesIO(data), self)

	def print_info(self, config):
		print("-------")
		print("DAG {:08X}".format(self.magic))
		if self.magic != self.MAGIC:
			print("[!] Unknown magic, should be {}".format(self.MAGIC))
		print("-------")
		print("")

		self.dat1.print_info(config)

		DEBUG_RANGE = range(40, 48)
		types = self.dat1.get_section(0x7A0266BC)
		pairs = self.dat1.get_section(0x933C0D32)
		names = self.dat1.get_section(0xD101A6CC)
		prnts = self.dat1.get_section(0xF958372E)

		if False:
			# some entries
			print("")
			print("Entries:")
			for i in DEBUG_RANGE:
				t, (a, b), n, p = types.entries[i], pairs.entries[i], names.entries[i], prnts.entries[i]

				name = self.dat1.get_string(n)
				if name is None:
					name = "<str at {}>".format(n)

				# print("  - {:<4}  {:016X}  {}".format(i, q[0], matfile if matfile is not None else "<str at {}>".format(self.string_offsets[i][0])))
				# print("          {:<8}{:08X}  {}".format(q[2], q[1], matname if matname is not None else "<str at {}>".format(self.string_offsets[i][1])))
				print("- {:<4}  {}".format(i, name[-64:]))
				print("        {:<8}  {:08X}  {:08X}  {:3}  {}".format(p, a, b, t, types.KNOWN_TYPES.get(t, '?')))
				print("")

		if False:
			# dependency chain for a file
			ndx = -1
			for i in range(len(prnts.entries)):
				t, (a, b), n, p = types.entries[i], pairs.entries[i], names.entries[i], prnts.entries[i]

				name = self.dat1.get_string(n)
				if name is None:
					name = "<str at {}>".format(n)
				
				if "hero_spiderman" in name and ".model" in name:
					ndx = i
					break

			while ndx != -1:
				i = ndx
				t, (a, b), n, p = types.entries[i], pairs.entries[i], names.entries[i], prnts.entries[i]
				ndx = p

				name = self.dat1.get_string(n)
				if name is None:
					name = "<str at {}>".format(n)

				print("")
				print("- {:<4}  {}".format(i, name[-64:]))
				print("        {:<8}  {:08X}  {:08X}  {:3}  {}".format(p, a, b, t, types.KNOWN_TYPES.get(t, '?')))

		if False:
			# reverse graph
			"""
			graph = {}
			cnt = len(prnts.entries)
			for i in range(cnt):
				p = prnts.entries[i]
				graph[p] = graph.get(p, []) + [i]
				print("{}%...".format(int(i * 1000.0 / cnt) * 0.1)		)

			print("files that have deps:", len(graph))
			print("files in root:", len(graph[-1]))
			"""

			print("")
			print("Building graph...")
			print("0 %                                          100 %") # 50 chars
			cnt = len(prnts.entries)
			root = []
			graph = []
			for i in range(cnt):
				graph += [[]]
			prev_percent = 0
			for i in range(cnt):
				p = prnts.entries[i]
				if p == -1:
					root += [i]
				else:
					try:
						graph[p] += [i]
					except:
						pass # TODO
				percent = i * 100 / cnt
				if percent > prev_percent and percent % 2 == 1:
					sys.stdout.write('.')
					sys.stdout.flush()
					prev_percent = percent
			print("")
			print("")


			"""
			files that have deps: 146619
			files in root: 268479
			 -1 (268479 children)
			   0 (1 children)
			   1 (0 children)
			   2 (1 children)
			   3 (0 children)
			   6 (0 children)
			   7 (1 children)
			   8 (0 children)
			   9 (0 children)
			   10 (0 children)
			"""

			print("files in root: ", len(root))
			print("other files: ", cnt - len(root))

			MAX_LEN = 0
			q = [(-1, -1)]
			lines_printed = 0
			while len(q) > 0:
				# v, q = q[0], q[1:]
				q, v = q[:-1], q[-1]
				v, depth = v
				# children = graph.get(v, [])
				children = []
				if v == -1:
					children = root
				elif v < len(graph):
					children = graph[v]				
				# print("  " * depth, v, "({} children)".format(len(children)))
				if v != -1:
					print("{}- {}: {}".format("  " * depth, v, self.dat1.get_string(names.entries[v])))
				lines_printed += 1
				q += [(c, depth+1) for c in children[::-1]]
				if lines_printed >= MAX_LEN:
					break
