# ALERT: Amazing Luna Engine Research Tools
# This program is free software, and can be redistributed and/or modified by you. It is provided 'as-is', without any warranty.
# For more details, terms and conditions, see GNU General Public License.
# A copy of the that license should come with this program (LICENSE.txt). If not, see <http://www.gnu.org/licenses/>.

from flask import request, Response
import json
import traceback

def _errmsg(e):
	msg = ""
	try:
		msg = e.message
	except:
		pass
	if msg == "":
		msg = str(e)
	return msg

def get_field(form, name):
	if name not in form:
		raise Exception("Missing '{}' field!".format(name))
	return form[name]

def get_int(form, name):
	return int(get_field(form, name))

def get_json(form, name):
	return json.loads(get_field(form, name))

def json_api(f, successful_response_is_json=True):
	ret = {"error": True, "message": "unknown error"}

	try:
		ret = f()
		if not successful_response_is_json:
			return ret
		ret["error"] = False
	except Exception as e:
		traceback.print_exc()
		ret = {"error": True, "message": _errmsg(e)}

	json_response = json.dumps(ret)
	return Response(json_response, 200, {'Content-Type': 'application/json'})

def make_get_route(app, route, f):
	decorated = lambda *args, **kwargs: f()
	decorated.__name__ = '_flask_handler_'+route.replace("/", "_")
	app.add_url_rule(route, view_func=decorated)
	
def make_post_route(app, route, f):
	decorated = lambda *args, **kwargs: f()
	decorated.__name__ = '_flask_handler_'+route.replace("/", "_")
	app.add_url_rule(route, methods=['POST'], view_func=decorated)

def json_api_wrapper(f, successful_response_is_json=True):
	return lambda *args, **kwargs: json_api(f, successful_response_is_json)

def make_get_json_route(app, route, f, successful_response_is_json=True):
	return make_get_route(app, route, json_api_wrapper(f, successful_response_is_json))

def make_post_json_route(app, route, f, successful_response_is_json=True):
	return make_post_route(app, route, json_api_wrapper(f, successful_response_is_json))
