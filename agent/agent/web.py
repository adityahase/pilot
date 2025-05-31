from quart import Quart, jsonify

from agent.hooks import startup

app = Quart(__name__)


@app.before_serving
async def agent_startup():
	await startup()


@app.route("/ping")
async def ping():
	return jsonify({"message": "pong"})
