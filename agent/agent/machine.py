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
		await self.run(f"cp {ARTIFACTS_ROOT}/ubuntu-24.04.ext4 {self.rootfs_file}")
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

	@classmethod
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

	@classmethod
	async def download_artifacts(cls, files):
		os.makedirs(os.path.join(CHROOT_PATH, ARTIFACTS_ROOT.lstrip("/")), exist_ok=True)
		for url, filename in files:
			file = os.path.join(CHROOT_PATH, ARTIFACTS_ROOT.lstrip("/"), filename)
			# Write the file to the host filesystem
			if not os.path.exists(file):
				await cls.download_file(url, file)

	@classmethod
	async def download_file(cls, url, filename):
		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(filename, "wb") as f:
				for chunk in r.iter_content(chunk_size=8192):
					f.write(chunk)

	@classmethod
	async def prepare_rootfs(cls, files):
		os.makedirs(os.path.join(CHROOT_PATH, ARTIFACTS_ROOT.lstrip("/")), exist_ok=True)

		async def unsquash_rootfs(squashfs_file, squashfs_root):
			await cls.run(f"unsquashfs -f -d {squashfs_root} {squashfs_file}")

		async def setup_ssh_key(ssh_key_file, squashfs_root):
			await cls.run(f'ssh-keygen -t ed25519 -f {ssh_key_file} -N ""')
			await cls.run(f"cp {ssh_key_file}.pub {squashfs_root}/root/.ssh/authorized_keys")

		async def setup_dns(squashfs_root):
			resolv_conf_path = os.path.join(CHROOT_PATH, squashfs_root.lstrip("/"), "etc/resolv.conf")
			with open(resolv_conf_path, "w") as f:
				f.write("nameserver 8.8.8.8")

		async def make_ext4_filesystem(squashfs_root, rootfs_file):
			await cls.run(f"chown -R root:root {squashfs_root}")
			await cls.run(f"truncate -s 400M {rootfs_file}")
			await cls.run(f"mkfs.ext4 -d {squashfs_root} -F {rootfs_file}")

		async def cleanup_temporary_files():
			await cls.run(f"rm -rf {squashfs_root}")

		for file in files:
			name = file.rsplit(".", 1)[0]
			squashfs_file = os.path.join(ARTIFACTS_ROOT, file)
			squashfs_root = os.path.join(ARTIFACTS_ROOT, f"{name}-squashfs")
			rootfs_file = os.path.join(ARTIFACTS_ROOT, f"{name}.ext4")
			ssh_key_file = os.path.join(ARTIFACTS_ROOT, f"{name}-id_ed25519")

			if os.path.exists(os.path.join(CHROOT_PATH, rootfs_file.lstrip("/"))):
				continue

			await unsquash_rootfs(squashfs_file, squashfs_root)

			if os.path.exists(os.path.join(CHROOT_PATH, ssh_key_file.lstrip("/"))):
				await setup_ssh_key(ssh_key_file, squashfs_root)

			await setup_dns(squashfs_root)
			await make_ext4_filesystem(squashfs_root, rootfs_file)
			await cleanup_temporary_files()


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
