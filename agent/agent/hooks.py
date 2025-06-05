from agent.machine import Machine
from agent.network import FirecrackerBridge
from agent.ubuntu import Ubuntu

EGRESS_INTERFACE = "eth0"


async def startup():
	bridge = FirecrackerBridge(egress_interface=EGRESS_INTERFACE)
	await bridge.setup()

	artifacts = [
		(
			"https://s3.amazonaws.com/spec.ccfc.min/firecracker-ci/v1.12/x86_64/vmlinux-6.1.128",
			"vmlinux-6.1.128",
		),
		(
			"https://s3.amazonaws.com/spec.ccfc.min/firecracker-ci/v1.12/x86_64/ubuntu-24.04.squashfs",
			"ubuntu-24.04.squashfs",
		),
	]
	await Machine.download_artifacts(artifacts)
	rootfs = [
		"ubuntu-24.04.squashfs",
	]
	await Machine.prepare_rootfs(rootfs)

	releases = [
		"focal",
		"noble",
	]
	await Ubuntu.setup_images(releases)
