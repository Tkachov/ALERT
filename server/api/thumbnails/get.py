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
		aid = request.args.get("aid", None)
		if aid is None:
			raise Exception("Missing 'aid' field!")

		return db.get_thumbnail(aid)

	except Exception as e:
		traceback.print_exc()
		ret = {"error": True, "message": _errmsg(e)}

	json_response = json.dumps(ret)
	return Response(json_response, 200, {'Content-Type': 'application/json'})
