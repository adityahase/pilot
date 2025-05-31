from agent.network import FirecrackerBridge

EGRESS_INTERFACE = "eth0"


async def startup():
	bridge = FirecrackerBridge(egress_interface=EGRESS_INTERFACE)
	await bridge.setup()
