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
		index = request.form.get("index", None)
		if index is None:
			raise Exception("Missing 'index' field!")

		asset, sz = db.extract_asset(int(index))
		ret = {"error": False, "asset": make_asset_details_json(asset, sz)}

	except Exception as e:
		traceback.print_exc()
		ret = {"error": True, "message": _errmsg(e)}

	json_response = json.dumps(ret)
	return Response(json_response, 200, {'Content-Type': 'application/json'})

def make_asset_details_json(asset, sz):
	return {
		"type": asset.__class__.__name__,
		"magic": asset.MAGIC,
		"sections": len(asset.dat1.sections),
		"size": sz
	}
