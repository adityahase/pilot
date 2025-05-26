from quart import Quart, jsonify

app = Quart(__name__)


@app.route("/ping")
async def ping():
	return jsonify({"message": "pong"})
