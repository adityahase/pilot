from quart import Quart, jsonify, request

from agent.hooks import startup
from agent.machine import Machine

app = Quart(__name__)


@app.before_serving
async def agent_startup():
	await startup()


@app.route("/ping")
async def ping():
	return jsonify({"message": "pong"})


@app.route("/machines", methods=["POST"])
async def create_machine():
	data = await request.json
	machine = await Machine.create(data)
	await machine.setup()
	await machine.start()
	return jsonify({"name": machine.name})
