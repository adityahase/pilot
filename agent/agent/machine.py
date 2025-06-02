import asyncio
import json
import os
import shlex

import requests

JAILER_ROOT = "/srv/jailer"
FIRECRACKER_BINARY = "/usr/local/bin/firecracker"
ARTIFACTS_ROOT = "/srv/artefacts"
CHROOT_PATH = "/host"


class SubprocessError(Exception):
	pass


class Machine:
	def __init__(self, id: str):
		self.id = id
		self.root = f"{JAILER_ROOT}/firecracker/{self.id}/root"
		self.config_file = f"{self.root}/config.json"
		self.kernel_file = f"{self.root}/vmlinux.bin"
		self.rootfs_file = f"{self.root}/rootfs.ext4"
		self.squashfs_root = f"{self.root}/squashfs-root"
		self.api_socket = f"{self.root}/firecracker.socket"
		self.private_key_file = f"{self.root}/id_ed25519"

		self.uid = 1000  # User ID for the jailer
		self.gid = 1000  # Group ID for the jailer

	async def setup(self):
		root = os.path.join(CHROOT_PATH, self.root.lstrip("/"))
		os.makedirs(root, exist_ok=True)
		await self.setup_config(json.loads(JSON))
		await self.setup_kernel()
		await self.setup_rootfs()
		await self.setup_tap_device()

	async def setup_config(self, config: dict):
		os.makedirs(os.path.join(CHROOT_PATH, self.root.lstrip("/")), exist_ok=True)
		config_file = os.path.join(CHROOT_PATH, self.config_file.lstrip("/"))
		with open(config_file, "w") as f:
			json.dump(config, f, indent=4)

	async def setup_kernel(self):
		await self.run(f"cp {ARTIFACTS_ROOT}/vmlinux-6.1.128 {self.kernel_file}")

	async def setup_rootfs(self):
		await self.run(f"unsquashfs -f -d {self.squashfs_root} {ARTIFACTS_ROOT}/ubuntu-24.04.squashfs")
		await self.setup_ssh_key()
		await self.setup_dns()
		await self.make_ext4_filesystem()

	async def setup_ssh_key(self):
		await self.run('ssh-keygen -t ed25519 -f id_ed25519 -N ""')
		await self.run(f"mv id_ed25519.pub {self.squashfs_root}/root/.ssh/authorized_keys")
		await self.run(f"mv id_ed25519 {self.private_key_file}")

	async def setup_dns(self):
		resolv_conf_path = os.path.join(CHROOT_PATH, self.squashfs_root.lstrip("/"), "etc/resolv.conf")
		with open(resolv_conf_path, "w") as f:
			f.write("nameserver 8.8.8.8")

	async def make_ext4_filesystem(self):
		await self.run(f"chown -R root:root {self.squashfs_root}")
		await self.run(f"truncate -s 400M {self.rootfs_file}")
		await self.run(f"mkfs.ext4 -d {self.squashfs_root} -F {self.rootfs_file}")
		await self.run(f"chown {self.uid}:{self.gid} {self.rootfs_file}")
		await self.run(f"chmod 600 {self.rootfs_file}")

	async def setup_tap_device(self):
		try:
			await self.run("ip link del tap0")
		except Exception:
			pass
		await self.run("ip tuntap add dev tap0 mode tap")
		await self.run("ip link set dev tap0 master firecracker0")
		await self.run("ip link set dev tap0 up")

	async def start(self):
		command = (
			f"jailer --id {self.id} --uid {self.uid} --gid {self.gid} "
			f"--daemonize --exec-file {FIRECRACKER_BINARY} "
			f"--chroot-base-dir {JAILER_ROOT} "
			f"-- --api-sock firecracker.socket --config-file config.json"
		)
		await self.run(command)

	async def run(self, cmd):
		args = shlex.split(cmd)
		args = ["chroot", CHROOT_PATH, *args]
		process = await asyncio.create_subprocess_exec(
			*args,
			stdin=asyncio.subprocess.DEVNULL,
			stderr=asyncio.subprocess.PIPE,
			stdout=asyncio.subprocess.PIPE,
		)
		await process.wait()
		if process.returncode != 0:
			raise SubprocessError
		return process


async def download_file(url, filename):
	with requests.get(url, stream=True) as r:
		r.raise_for_status()
		with open(filename, "wb") as f:
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)


async def download_artifacts():
	os.makedirs(os.path.join(CHROOT_PATH, ARTIFACTS_ROOT.lstrip("/")), exist_ok=True)
	files = [
		(
			"https://s3.amazonaws.com/spec.ccfc.min/firecracker-ci/v1.12/x86_64/vmlinux-6.1.128",
			"vmlinux-6.1.128",
		),
		(
			"https://s3.amazonaws.com/spec.ccfc.min/firecracker-ci/v1.12/x86_64/ubuntu-24.04.squashfs",
			"ubuntu-24.04.squashfs",
		),
	]
	for url, filename in files:
		file = os.path.join(CHROOT_PATH, ARTIFACTS_ROOT.lstrip("/"), filename)
		# Write the file to the host filesystem
		if not os.path.exists(file):
			await download_file(url, file)


JSON = """{
	"boot-source": {
			"kernel_image_path": "vmlinux.bin",
			"boot_args": "console=ttyS0 reboot=k panic=1 pci=off ip=10.0.0.10::10.0.0.1:255.255.255.0::eth0:off",
			"initrd_path": null
	},
	"drives": [
			{
					"drive_id": "rootfs",
					"partuuid": null,
					"is_root_device": true,
					"cache_type": "Unsafe",
					"is_read_only": false,
					"path_on_host": "rootfs.ext4",
					"io_engine": "Sync",
					"rate_limiter": null,
					"socket": null
			}
	],
	"machine-config": {
			"vcpu_count": 2,
			"mem_size_mib": 1024,
			"smt": false,
			"track_dirty_pages": false,
			"huge_pages": "None"
	},
	"cpu-config": null,
	"balloon": null,
	"network-interfaces": [
			{
					"iface_id": "pilot0",
					"guest_mac": "02:FC:00:00:00:05",
					"host_dev_name": "tap0"
			}
	],
	"vsock": null,
	"logger": null,
	"metrics": null,
	"mmds-config": null,
	"entropy": null
}
"""
