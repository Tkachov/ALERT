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
		toc_path = request.form.get("toc_path", None)
		if toc_path is None:
			raise Exception("Missing 'toc_path' field!")

		db.load_toc(toc_path)
		ret = {"error": False, "toc": make_toc_json(db.toc)}

	except Exception as e:
		traceback.print_exc()
		ret = {"error": True, "message": _errmsg(e)}

	json_response = json.dumps(ret)
	return Response(json_response, 200, {'Content-Type': 'application/json'})

def make_toc_json(toc):
	archives = toc.get_archives_section()
	assets = toc.get_assets_section()
	return {
		"archives": len(archives.archives),
		"assets": len(assets.ids)
	}
