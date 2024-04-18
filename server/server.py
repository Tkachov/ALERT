# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

import sys
import os
from flask import Flask, url_for, send_from_directory, request, Response
import importlib
from functools import wraps

from server.state import State

app = None

def print_self(filename):
	try:
		from pefile import PE

		name = None
		version = None

		pe = PE(filename)
		for i in range(len(pe.FileInfo)):
			try:
				fi = pe.FileInfo[i]
				for j in range(len(fi)):
					try:
						content = fi[j]
						sts = content.StringTable
						for st in sts:
							for k, v in st.entries.items():
								if k == b"ProductName":
									name = v
								elif k == b"ProductVersion":
									version = v
					except:
						pass
			except:
				pass

		if name is not None:
			if version is not None:
				print(" * {} v. {}".format(name.decode('ascii'), version.decode('ascii')))
			else:
				print(" *", name)
	except:
		pass

if getattr(sys, 'frozen', False):
	print_self(sys.argv[0])
	print(" *", sys._MEIPASS)
	print("")
	app = Flask(__name__, static_folder=os.path.join(sys._MEIPASS, 'static'))
else:
	app = Flask(__name__)

# API

state = State(app)

# static stuff

@app.route('/')
def index():
	return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def send_static(path):
	r = send_from_directory(app.static_folder, path)
	
	ct = None
	if path.endswith(".js"):
		ct = "application/javascript; charset=utf-8"
	elif path.endswith(".ico"):
		ct = "image/x-icon"

	if ct is not None:
		r.headers['Content-Type'] = ct

	return r

# error handling

@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def http_error_handler(error):	
	return send_from_directory(app.static_folder, "%d.html" % error.code), error.code
