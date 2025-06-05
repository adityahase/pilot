from agent.images.firecracker import Firecracker
from agent.images.ubuntu import Ubuntu
from agent.network import FirecrackerBridge

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
	await Firecracker.download_artifacts(artifacts)
	rootfs = [
		"ubuntu-24.04.squashfs",
	]
	await Firecracker.prepare_rootfs(rootfs)

	releases = [
		"focal",
		"noble",
	]
	await Ubuntu.setup_images(releases)
