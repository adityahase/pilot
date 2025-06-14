import asyncio
import shlex

from agent.machine import CHROOT_PATH, SubprocessError


class FirecrackerBridge:
	def __init__(self, egress_interface):
		self.name = "firecracker0"
		self.cidr = "10.0.0.1/24"
		self.egress_interface = egress_interface

	async def setup(self):
		await self.setup_bridge()
		await self.setup_forwarding()
		await self.setup_masquerading()

	async def setup_bridge(self):
		if await self.bridge_exists():
			return
		else:
			commands = [
				# Create the bridge interface
				f"ip link add name {self.name} type bridge",
				# Assign IP address to the bridge
				f"ip addr add {self.cidr} dev {self.name}",
				# Bring the bridge interface up
				f"ip link set dev {self.name} up",
			]
			for cmd in commands:
				await self.run(cmd)

	async def bridge_exists(self):
		try:
			await self.run(f"ip link show {self.name}")
			return True
		except SubprocessError:
			return False

	async def setup_forwarding(self):
		await self.run("sysctl -w net.ipv4.ip_forward=1")
		await self.run("iptables -P FORWARD ACCEPT")
		if not await self.is_forwarding():
			await self.run(f"iptables --insert FORWARD --in-interface {self.name} -j ACCEPT")

	async def is_forwarding(self):
		try:
			await self.run(f"iptables --check FORWARD --in-interface {self.name} -j ACCEPT")
			return True
		except SubprocessError:
			return False

	async def setup_masquerading(self):
		if not await self.is_masquerading():
			await self.run(
				"iptables --table nat --append POSTROUTING "
				f"--out-interface {self.egress_interface} -j MASQUERADE"
			)

	async def is_masquerading(self):
		try:
			await self.run(
				"iptables --table nat --check POSTROUTING "
				f"--out-interface {self.egress_interface} -j MASQUERADE"
			)
			return True
		except SubprocessError:
			return False

	async def run(self, cmd):
		args = shlex.split(cmd)
		args = ["chroot", CHROOT_PATH, *args]
		print(f"Command: {cmd}")
		process = await asyncio.create_subprocess_exec(
			*args,
			stdin=asyncio.subprocess.DEVNULL,
			stderr=asyncio.subprocess.PIPE,
			stdout=asyncio.subprocess.PIPE,
		)
		await process.wait()
		if process.returncode != 0:
			print(f"Command finished with return code {process.returncode}")
			print(f"Command output: {await process.stdout.read()}")
			print(f"Command error: {await process.stderr.read()}")
			raise SubprocessError
		return process
