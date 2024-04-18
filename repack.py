# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import sys

import dat1lib
import dat1lib.types.dat1
import dat1lib.types.model

###

def main(argv):
	if len(argv) < 2:
		print("Usage:")
		print("$ {} <filename>".format(argv[0]))
		print("")
		print("Read the .model and save it as .model.repacked")
		print("Resulting file should work in game as usual")
		return

	#

	fn = argv[1]
	model = None
	try:
		with open(fn, "rb") as f:
			model = dat1lib.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(fn))
		print(e)
		return

	#
	
	if model is None:
		print("[!] Couldn't comprehend '{}'".format(fn))
		return

	if not isinstance(model, dat1lib.types.model.Model): # TODO: should 'repack' only work on models?
		print("[!] Not a model")
		return

	#

	model.dat1.set_recalculation_strategy(dat1lib.types.dat1.RECALCULATE_ORIGINAL_ORDER)
	model.dat1.recalculate_section_headers()

	with open(fn + ".repacked", "wb") as f:
		model.save(f)

if __name__ == "__main__":
	main(sys.argv)
