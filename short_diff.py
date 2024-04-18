# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib
import hashlib
import sys
import traceback

#

def get_md5(fn):
	hash_md5 = hashlib.md5()
	with open(fn, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def print_info(fn, o):
	h = get_md5(fn)
	print(fn)
	print(h)
	try:
		print("{} ({:08X}), {} sections".format(o.__class__.__name__, o.magic, len(o.dat1.sections)))
	except:
		print("?")
	return h

def get_sections_set(o):
	s = o.dat1.header.sections
	return set([x.tag for x in s])

def diff_containers(o1, o2):
	sections1 = get_sections_set(o1)
	sections2 = get_sections_set(o2)

	for s in o1.dat1.header.sections:
		tag = s.tag
		if tag not in sections2:
			print("{:08X} -- only in first".format(tag))
			print()
			continue

		were_diffs = False

		s1 = o1.dat1.get_section(tag)
		s2 = o2.dat1.get_section(tag)
		sf1 = s1.get_short_suffix() if s1 is not None else "-"
		sf2 = s2.get_short_suffix() if s2 is not None else "-"

		if sf1 != sf2:
			if not were_diffs: # always True
				print("{:08X} -- {}/{}".format(tag, sf1, sf2))
				were_diffs = True

		d1 = o1.dat1._sections_data[o1.dat1._sections_map[tag]]
		d2 = o2.dat1._sections_data[o2.dat1._sections_map[tag]]

		if len(d1) != len(d2):
			if not were_diffs:
				print("{:08X} -- {}".format(tag, sf1))
				were_diffs = True
			print("\tdifferent length: {} vs {}".format(len(d1), len(d2)))
		
		if len(d1) == len(d2) and d1 != d2:
			if not were_diffs:
				print("{:08X} -- {}".format(tag, sf1))
				were_diffs = True
			print("\tdifferent content")


	for s in o2.dat1.header.sections:
		tag = s.tag
		if tag in sections1:
			continue # already diffed up there
		if tag not in sections1:
			print("{:08X} -- only in second".format(tag))
			print()
			continue

#

def main(argv):
	if len(argv) < 3:
		print("Usage:")
		print("$ {} <filename> <filename>".format(argv[0]))
		print("")
		print("Compare the two files")
		return

	#

	fn1 = argv[1]
	fn2 = argv[2]
	o1 = None
	o2 = None

	try:
		with open(fn1, "rb") as f:
			o1 = dat1lib.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(fn1))
		print(e)
		traceback.print_exc()
		return

	try:
		with open(fn2, "rb") as f:
			o2 = dat1lib.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(fn2))
		print(e)
		traceback.print_exc()
		return

	#
	
	if o1 is None:
		print("[!] Couldn't comprehend '{}'".format(fn1))
		return

	if o2 is None:
		print("[!] Couldn't comprehend '{}'".format(fn2))
		return

	#

	print()
	h1 = print_info(fn1, o1)
	print("----")
	h2 = print_info(fn2, o2)
	print()

	if h1 == h2:
		print("Assuming equal")
		return
	
	diff_containers(o1, o2)

if __name__ == "__main__":
	main(sys.argv)	
