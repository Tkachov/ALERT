# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import sys

def path_without_extension(s):
	i = s.rfind(".")
	if i == -1:
		return s
	else:
		return s[:i]

if __name__ == "__main__":
	argv = sys.argv
	if len(argv) < 2:
		print("Usage:")
		print("$ {} <.model filename>".format(argv[0]))
		sys.exit(1)

	model_fn = argv[1]
	ascii_fn = path_without_extension(model_fn) + ".ascii"
	mats_txt = path_without_extension(model_fn) + "_materials.txt"
	new_argv = argv[:2] + [ascii_fn, mats_txt]

	import model_to_ascii
	model_to_ascii.main(new_argv)
