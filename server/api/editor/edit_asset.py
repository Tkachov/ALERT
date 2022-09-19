from flask import Response, send_file
import io
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

def handle(request, db):
	ret = {"error": True, "message": "unknown error"}

	try:
		index = get_int(request.form, "index")
		header = get_json(request.form, "header")
		strings = get_json(request.form, "strings")
		sections = get_json(request.form, "sections")

		if strings["option"] == "replace":
			strings["raw"] = request.files["strings_raw"].read()

		for s in sections:
			if s["option"] == "replace":
				s["raw"] = request.files["{:08X}_raw".format(s["tag"])].read()

		db.edit_asset(index, header, strings, sections)
		ret = {"error": False}

	except Exception as e:
		traceback.print_exc()
		ret = {"error": True, "message": _errmsg(e)}

	json_response = json.dumps(ret)
	return Response(json_response, 200, {'Content-Type': 'application/json'})
