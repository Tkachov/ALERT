# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib
import sys
import traceback

def main(argv):
	if len(argv) < 3:
		print("Usage:")
		print("$ {} <filename> <section index or tag>".format(argv[0]))
		print("")
		print("Read a supported file and extract specified section into a separate file.")
		return

	#

	fn = argv[1]
	obj = None
	try:
		with open(fn, "rb") as f:
			obj = dat1lib.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(fn))
		print(e)
		print(traceback.format_exc())
		return

	#
	
	if obj is None:
		print("[!] Couldn't comprehend '{}'".format(fn))
		return
	
	#

	i = argv[2]
	try:
		i = int(i)
	except:
		i = int(i, 16)

	if "dat1" in dir(obj):
		obj = obj.dat1

	s = None
	if i < len(obj.sections):
		s = obj.sections[i]
	else:
		s = obj.get_section(i)

	if s is None:
		print("[!] Section {:08X} was not found".format(i))
		return

	try:
		with open(fn + ".{:08X}".format(s.TAG), "wb") as f:
			f.write(s._raw)
	except Exception as e:
		print("[!] Failed")
		print(e)

if __name__ == "__main__":
	main(sys.argv)	
