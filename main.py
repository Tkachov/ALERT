# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import sys

import info
import extract_assets
import extract_section
import change_soundbank
import model_to_ascii
import ascii_to_model

def main(argv):
	scripts = {
		"info": info.main,
		"extract_assets": extract_assets.main,
		"extract_section": extract_section.main,
		"change_soundbank": change_soundbank.main,
		"model_to_ascii": model_to_ascii.main,
		"ascii_to_model": ascii_to_model.main
	}

	if len(argv) < 2 or argv[1] not in scripts:
		print("Usage:")
		print("$ {} [script] [args]".format(argv[0]))
		print("")
		print("Scripts:")
		print("  info                Print as much info about a file as possible")
		print("  extract_assets      Interactive assets extractor")
		print("  extract_section     Save a single section as file")
		print("  change_soundbank    Inject .bnk into .soundbank")
		print("  model_to_ascii      Write .ascii by .model")
		print("  ascii_to_model      Inject data from .ascii into .model")
		return

	#

	name = argv[1]
	entry_point = scripts[name]
	entry_point([name] + argv[2:])

if __name__ == "__main__":
	main(sys.argv)
