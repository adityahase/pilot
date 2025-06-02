from agent.machine import Machine, download_artifacts
from agent.network import FirecrackerBridge

EGRESS_INTERFACE = "eth0"


async def startup():
	bridge = FirecrackerBridge(egress_interface=EGRESS_INTERFACE)
	await bridge.setup()

	await download_artifacts()

	machine = Machine("1")
	await machine.setup()
	await machine.start()
