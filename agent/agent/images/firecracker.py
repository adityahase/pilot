import asyncio
import os
import shlex

import requests

from agent.machine import ARTIFACTS_ROOT, CHROOT_PATH, SubprocessError


class Firecracker:
	@classmethod
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
			rootfs_file = os.path.join(ARTIFACTS_ROOT, f"{name}.rootfs")
			ssh_key_file = os.path.join(ARTIFACTS_ROOT, f"{name}-id_ed25519")

			if os.path.exists(os.path.join(CHROOT_PATH, rootfs_file.lstrip("/"))):
				continue

			await unsquash_rootfs(squashfs_file, squashfs_root)

			if os.path.exists(os.path.join(CHROOT_PATH, ssh_key_file.lstrip("/"))):
				await setup_ssh_key(ssh_key_file, squashfs_root)

			await setup_dns(squashfs_root)
			await make_ext4_filesystem(squashfs_root, rootfs_file)
			await cleanup_temporary_files()
