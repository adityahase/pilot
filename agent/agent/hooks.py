from agent.images.firecracker import Firecracker
from agent.images.ubuntu import Ubuntu
from agent.network import FirecrackerBridge

EGRESS_INTERFACE = "eth0"


async def startup():
	bridge = FirecrackerBridge(egress_interface=EGRESS_INTERFACE)
	await bridge.setup()

	firecracker_artifacts = [
		(
			"https://s3.amazonaws.com/spec.ccfc.min/firecracker-ci/v1.12/x86_64/vmlinux-5.10.233",
			"ubuntu-24.04-firecracker-linux-5.x.kernel",
		),
		(
			"https://s3.amazonaws.com/spec.ccfc.min/firecracker-ci/v1.12/x86_64/vmlinux-6.1.128",
			"ubuntu-24.04-firecracker.kernel",
		),
		(
			"https://s3.amazonaws.com/spec.ccfc.min/firecracker-ci/v1.12/x86_64/ubuntu-24.04.squashfs",
			"ubuntu-24.04-firecracker.squashfs",
		),
	]
	await Firecracker.download_artifacts(firecracker_artifacts)
	firecracker_rootfs = [
		"ubuntu-24.04-firecracker.squashfs",
	]
	await Firecracker.prepare_rootfs(firecracker_rootfs)

	ubuntu_releases = [
		"focal",
		"jammy",
		"noble",
	]
	await Ubuntu.setup_images(ubuntu_releases)
