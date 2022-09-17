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

def handle(request, db):
	ret = {"error": True, "message": "unknown error"}

	try:
		index = request.args.get("index", None)
		if index is None:
			raise Exception("Missing 'index' field!")
		
		data, basename = db.get_asset_data(int(index))
		return send_file(io.BytesIO(data), as_attachment=True, attachment_filename=basename, mimetype='application/octet-stream')

	except Exception as e:
		traceback.print_exc()
		ret = {"error": True, "message": _errmsg(e)}

	json_response = json.dumps(ret)
	return Response(json_response, 200, {'Content-Type': 'application/json'})
