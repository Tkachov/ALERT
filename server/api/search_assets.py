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
		needle = request.form.get("needle", None)
		if needle is None:
			raise Exception("Missing 'needle' field!")

		if needle is None or needle == "":
			raise Exception("Empty search request, ignoring.")

		# for now only support hex asset ids
		# TODO: actual text search

		aid = None
		try:
			aid = int(needle, 16)
		except:
			pass

		if aid is None:
			raise Exception("Bad request.")

		entries = db.toc.get_asset_entries_by_assetid(aid)
		ret = {"error": False, "entries": [make_entry_json(e) for e in entries]}

	except Exception as e:
		traceback.print_exc()
		ret = {"error": True, "message": _errmsg(e)}

	json_response = json.dumps(ret)
	return Response(json_response, 200, {'Content-Type': 'application/json'})

def make_entry_json(e):
	return {
		"id": "{:016X}".format(e.asset_id),
		"index": e.index,
		"archive": e.archive,
		"offset": e.offset,
		"size": e.size
	}
