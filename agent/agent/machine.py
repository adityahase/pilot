import asyncio
import copy
import json
import os
import shlex

JAILER_ROOT = "/srv/jailer"
FIRECRACKER_BINARY = "/usr/local/bin/firecracker"
ARTIFACTS_ROOT = "/srv/artefacts"
CHROOT_PATH = "/host"
FIRECRACKER_DIRECTORY = "/var/lib/firecracker"


class SubprocessError(Exception):
	pass


class Machine:
	def __init__(self, name: str):
		self.name = name
		self.root = f"{JAILER_ROOT}/firecracker/{self.name}/root"
		self.config_file = f"{self.root}/config.json"
		self.kernel_file = f"{self.root}/vmlinux.bin"
		self.rootfs_file = f"{self.root}/rootfs.ext4"
		self.api_socket = f"{self.root}/firecracker.socket"
		self.initrd_file = f"{self.root}/initrd.img"
		self.stdout_file = f"{self.root}/stdout.log"
		self.stderr_file = f"{self.root}/stderr.log"
		self.config = {}

		self.uid = 1000  # User ID for the jailer
		self.gid = 1000  # Group ID for the jailer

	@classmethod
	async def create(cls, data: dict):
		name = data["name"]
		await cls.save(name, data)
		return Machine(name)

	@classmethod
	async def save(cls, name, data: dict):
		data_directory = os.path.join(CHROOT_PATH, FIRECRACKER_DIRECTORY.lstrip("/"))
		os.makedirs(data_directory, exist_ok=True)
		data_file = os.path.join(data_directory, f"{name}.json")
		with open(data_file, "w") as f:
			json.dump(data, f, indent=4)

	@classmethod
	async def load(cls, name: str):
		data_directory = os.path.join(CHROOT_PATH, FIRECRACKER_DIRECTORY.lstrip("/"))
		data_file = os.path.join(data_directory, f"{name}.json")
		with open(data_file) as f:
			data = json.load(f)
		return data

	async def get_config_from_data(self):
		data = await self.load(self.name)
		self.config = data
		config = copy.deepcopy(DEFAULT_CONFIG)
		network = data.get("network")
		boot = data.get("boot")
		config["boot-source"]["boot_args"] += (
			f" ip={network['ip_address']}::{network['gateway']}:{network['subnet_mask']}::pilot0:off"
		)
		if boot.get("initial_ram_disk"):
			# Not all machines use an initrd, so we check if it is needed
			# Ubuntu cloud images need initrd
			config["boot-source"]["initrd_path"] = "initrd.img"
		config["network-interfaces"] = [
			{
				"iface_id": "pilot0",
				"guest_mac": network["mac_address"],
				"host_dev_name": network["tap_device"],
			}
		]
		config["machine-config"].update(
			{
				"vcpu_count": data["resources"]["vcpu"],
				"mem_size_mib": data["resources"]["memory"],
			}
		)
		return config

	async def setup(self):
		root = os.path.join(CHROOT_PATH, self.root.lstrip("/"))
		os.makedirs(root, exist_ok=True)
		await self.setup_config(await self.get_config_from_data())
		await self.setup_kernel()
		await self.setup_initrd()
		await self.setup_rootfs()
		await self.setup_tap_device()

	async def setup_config(self, config: dict):
		os.makedirs(os.path.join(CHROOT_PATH, self.root.lstrip("/")), exist_ok=True)
		config_file = os.path.join(CHROOT_PATH, self.config_file.lstrip("/"))
		with open(config_file, "w") as f:
			json.dump(config, f, indent=4)

	async def setup_kernel(self):
		boot = self.config.get("boot", {})
		self.kernel_source = os.path.join(ARTIFACTS_ROOT, boot.get("kernel"))
		await self.run(f"cp {self.kernel_source} {self.kernel_file}")

	async def setup_initrd(self):
		boot = self.config.get("boot", {})
		if not boot.get("initial_ram_disk"):
			return
		self.initrd_source = os.path.join(ARTIFACTS_ROOT, boot.get("initial_ram_disk"))
		await self.run(f"cp {self.initrd_source} {self.initrd_file}")

	async def setup_rootfs(self):
		boot = self.config.get("boot", {})
		self.rootfs_source = os.path.join(ARTIFACTS_ROOT, boot.get("root_filesystem"))
		await self.run(f"cp {self.rootfs_source} {self.rootfs_file}")
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
			"systemd-run "
			f"--property=StandardOutput=file:{self.stdout_file} "
			f"--property=StandardError=file:{self.stderr_file} "
			f"jailer --id {self.name} --uid {self.uid} --gid {self.gid} "
			f"--exec-file {FIRECRACKER_BINARY} "
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


DEFAULT_CONFIG = {
	"boot-source": {
		"kernel_image_path": "vmlinux.bin",
		"boot_args": "console=ttyS0 reboot=k panic=1 pci=off",
	},
	"drives": [
		{
			"drive_id": "rootfs",
			"is_root_device": True,
			"cache_type": "Unsafe",
			"is_read_only": False,
			"path_on_host": "rootfs.ext4",
			"io_engine": "Sync",
		}
	],
	"machine-config": {
		"vcpu_count": 1,
		"mem_size_mib": 512,
		"smt": False,
		"track_dirty_pages": False,
	},
}
