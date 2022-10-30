from flask import Response
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

def handle(request, db):
	ret = {"error": True, "message": "unknown error"}

	try:
		index = request.args.get("index", None)
		if index is None:
			raise Exception("Missing 'index' field!")

		mmi = request.args.get("mipmap_index", None)
		if mmi is None:
			raise Exception("Missing 'mipmap_index' field!")

		return db.get_texture_mipmap(int(index), int(mmi))

	except Exception as e:
		traceback.print_exc()
		ret = {"error": True, "message": _errmsg(e)}

	json_response = json.dumps(ret)
	return Response(json_response, 200, {'Content-Type': 'application/json'})
