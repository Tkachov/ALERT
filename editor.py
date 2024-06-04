# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import sys

if __name__ == "__main__":
	no_args = (len(sys.argv) < 2)
	custom_mode = False

	if not no_args:
		if sys.argv[1] == "so":
			import dat1lib
			dat1lib.VERSION_OVERRIDE = dat1lib.VERSION_SO
			custom_mode = True

		elif sys.argv[1] == "msmr":
			import dat1lib
			dat1lib.VERSION_OVERRIDE = dat1lib.VERSION_MSMR
			custom_mode = True

		elif sys.argv[1] == "-try-second-magic":
			import dat1lib
			dat1lib.TRY_SECOND_MAGIC = True
			custom_mode = True			

	if no_args or custom_mode:			
		from server.server import app
		app.run(host='0.0.0.0', port=55555)
	else:
		import main
		main.main(sys.argv)
