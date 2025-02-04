# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import dat1lib
import dat1lib.types.soundbank
import sys

def main(argv):
	if len(argv) < 3:
		print("Usage:")
		print("$ {} <.soundbank filename> <.bnk filename>".format(argv[0]))
		print("")
		print("Read the .soundbank, replace the .bnk in it with one provided")
		print("And save as .soundbank.edited")
		return

	#

	fn = argv[1]
	sb = dat1lib.read_stg(fn, dat1lib.types.soundbank.Soundbank.MAGIC)

	if sb is None:
		print("[!] Couldn't comprehend '{}'".format(fn))
		return

	if not isinstance(sb, dat1lib.types.soundbank.Soundbank):
		print("[!] Not a soundbank")
		return

	#

	bnk_fn = argv[2]
	data = None
	try:
		with open(bnk_fn, "rb") as f:
			data = f.read()
	except Exception as e:
		print("[!] Couldn't open '{}'".format(bnk_fn))
		print(e)
		return

	#

	sb.replace_wwise_bank_section(data)

	with open(fn + ".edited", "wb") as f:
		sb.save(f)

if __name__ == "__main__":
	main(sys.argv)
