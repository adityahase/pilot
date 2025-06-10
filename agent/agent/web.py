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


@app.route("/machines/<string:name>/actions/stop", methods=["POST"])
async def stop_machine(name):
	await Machine(name).stop()
	return jsonify({"name": name})


@app.route("/machines/<string:name>", methods=["DELETE"])
async def terminate_machine(name):
	await Machine(name).terminate()
	return jsonify({"name": name})
