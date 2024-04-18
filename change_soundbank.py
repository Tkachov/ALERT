# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import sys

import dat1lib
import dat1lib.types.dat1
import dat1lib.types.soundbank
import dat1lib.types.sections.soundbank.bnk

###

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
	sb = None
	try:
		with open(fn, "rb") as f:
			sb = dat1lib.read(f)
	except Exception as e:
		print("[!] Couldn't open '{}'".format(fn))
		print(e)
		return

	#
	
	if sb is None:
		print("[!] Couldn't comprehend '{}'".format(fn))
		return

	if not isinstance(sb, dat1lib.types.soundbank.Soundbank) and not isinstance(sb, dat1lib.types.soundbank.SoundbankRcra):
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

	if data is None:
		print("[!] Couldn't read '{}'".format(bnk_fn))

	#

	BNK_SECTION = dat1lib.types.sections.soundbank.bnk.WwiseBankSection.TAG
	sb.dat1.get_section(BNK_SECTION).replace_data(data)
	sb.dat1.refresh_section_data(BNK_SECTION)
	sb.dat1.recalculate_section_headers()

	with open(fn + ".edited", "wb") as f:
		sb.save(f)

if __name__ == "__main__":
	main(sys.argv)
