# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib
import sys

CONFIG = {
	"sections": True,
	"sections_verbose": True
}

def main(argv):
	if len(argv) < 2:
		print("Usage:")
		print("$ {} <filename>".format(argv[0]))
		print("")
		print("Read the file (could be 'toc', 'dag', '.model' or any '1TAD')")
		print("and print as much info about it as possible")
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
		return

	#
	
	if obj is None:
		print("[!] Couldn't comprehend '{}'".format(fn))
		return
	
	obj.print_info(CONFIG)

if __name__ == "__main__":
	main(sys.argv)	
