import asyncio
import copy
import json
import os
import shlex
import shutil
import tempfile

import requests_unixsocket

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
		self.tap_device = None
		self.config = {}

	@classmethod
	async def create(cls, data: dict):
		name = data["name"]
		await cls.save(name, data)
		return Machine(name)

	async def terminate(self):
		try:
			await self.stop()
		except Exception as e:
			print(f"Error stopping machine {self.name}: {e}")
		await self.cleanup()

	async def stop(self):
		response = self.client.put("/actions", {"action_type": "SendCtrlAltDel"})
		return response

	async def cleanup(self):
		# Remove jailer root directotry
		root = os.path.join(CHROOT_PATH, self.root.lstrip("/"))
		shutil.rmtree(os.path.dirname(root))

		await self.get_config_from_data()
		await self.delete_tap_device()

		state_file = os.path.join(CHROOT_PATH, FIRECRACKER_DIRECTORY.lstrip("/"), f"{self.name}.json")
		# Remove machine state file
		os.remove(state_file)

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

		isolation = data["isolation"]
		self.uid = isolation["user_id"]
		self.gid = isolation["group_id"]

		config = copy.deepcopy(DEFAULT_CONFIG)
		network = data.get("network")
		self.tap_device = network["tap_device"]
		boot = data.get("boot")
		if "meta-data" not in data:
			config["drives"].append(
				{
					"drive_id": "cloud-init",
					"is_root_device": False,
					"is_read_only": True,
					"path_on_host": "cloud-init.vfat",
				}
			)
		else:
			# If meta-data is not provided then we'll depend on cloud-init to configure the machine
			config["boot-source"]["boot_args"] += (
				f" ip={network['ip_address']}::{network['gateway']}:{network['subnet_mask']}::eth0:off"
			)
		if boot.get("initial_ram_disk"):
			# Not all machines use an initrd, so we check if it is needed
			# Ubuntu cloud images need initrd
			config["boot-source"]["initrd_path"] = "initrd.img"
		config["network-interfaces"] = [
			{
				"iface_id": "eth0",
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
		await self.setup_metadata()
		await self.setup_kernel()
		await self.setup_initrd()
		await self.setup_rootfs()
		await self.setup_tap_device()

	async def setup_config(self, config: dict):
		os.makedirs(os.path.join(CHROOT_PATH, self.root.lstrip("/")), exist_ok=True)
		config_file = os.path.join(CHROOT_PATH, self.config_file.lstrip("/"))
		with open(config_file, "w") as f:
			json.dump(config, f, indent=4)

	async def setup_metadata(self):
		# Assumes config is already loaded
		metadata = self.config.get("meta-data")
		if metadata:
			await self.setup_cloud_init(metadata)

	async def setup_cloud_init(self, metadata: dict):
		cloud_init_image = os.path.join(self.root, "cloud-init.vfat")

		await self.run(f"truncate -s 1M {cloud_init_image}")
		await self.run(f"mkfs.vfat -n 'cidata' {cloud_init_image}")

		with tempfile.TemporaryDirectory(
			prefix="cloud-init",
			dir=os.path.join(CHROOT_PATH, self.root.lstrip("/")),
			ignore_cleanup_errors=True,
		) as tempdir:
			temp = "/".join(tempdir.split("/")[2:])
			await self.run(f"mount -o loop {cloud_init_image} {temp}")

			for key, value in metadata.items():
				if not value:
					continue
				with open(os.path.join(tempdir, key), "w") as f:
					f.write(value)

			await self.run(f"umount {temp}")

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
		await self.run(f"ip tuntap add dev {self.tap_device} mode tap")
		await self.run(f"ip link set dev {self.tap_device} master firecracker0")
		await self.run(f"ip link set dev {self.tap_device} up")

	async def delete_tap_device(self):
		try:
			await self.run(f"ip link del {self.tap_device}")
		except Exception as e:
			print(f"Error deleting tap device {self.tap_device}: {e}")

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

	@property
	def client(self):
		return FirecrackerClient(os.path.join(CHROOT_PATH, self.api_socket.lstrip("/")))


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


class FirecrackerClient:
	def __init__(self, socket):
		self.session = requests_unixsocket.Session()
		self.base_url = f"http+unix://{socket.replace('/', '%2F')}"

	def get(self, endpoint):
		return self.session.get(f"{self.base_url}{endpoint}")

	def put(self, endpoint, json=None):
		return self.session.put(f"{self.base_url}{endpoint}", json=json)

	def patch(self, endpoint, json=None):
		return self.session.patch(f"{self.base_url}{endpoint}", json=json)

	def post(self, endpoint, json=None):
		return self.session.post(f"{self.base_url}{endpoint}", json=json)
