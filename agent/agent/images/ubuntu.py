import asyncio
import copy
import json
import os
import shlex
import tempfile

import requests

from agent.machine import ARTIFACTS_ROOT, CHROOT_PATH, SubprocessError

UBUNTU_RELEASES = {
	"focal": "20.04",
	"jammy": "22.04",
	"noble": "24.04",
}


class Ubuntu:
	@classmethod
	async def run(cls, cmd, shell=False):
		cmd = f"chroot {CHROOT_PATH} {cmd}"
		print(f"Running command: {cmd}")
		if shell:
			process = await asyncio.create_subprocess_shell(
				cmd,
				stdin=asyncio.subprocess.DEVNULL,
				stderr=asyncio.subprocess.PIPE,
				stdout=asyncio.subprocess.PIPE,
			)
		else:
			args = shlex.split(cmd)
			process = await asyncio.create_subprocess_exec(
				*args,
				stdin=asyncio.subprocess.DEVNULL,
				stderr=asyncio.subprocess.PIPE,
				stdout=asyncio.subprocess.PIPE,
			)
		await process.wait()
		if process.returncode != 0:
			print(f"Command failed: {cmd}")
			print(f"Return code: {process.returncode}")
			print(f"Error output: {await process.stderr.read()}")
			print(f"Standard output: {await process.stdout.read()}")
			raise SubprocessError
		return process

	@classmethod
	async def setup_images(cls, releases):
		os.makedirs(os.path.join(CHROOT_PATH, ARTIFACTS_ROOT.lstrip("/")), exist_ok=True)
		await cls.setup_extract_vmlinux()
		for release in releases:
			await cls.download_files(release)
			await cls.prepare_files(release)

	@classmethod
	async def setup_extract_vmlinux(cls):
		extract_script = os.path.join(CHROOT_PATH, ARTIFACTS_ROOT.lstrip("/"), "extract-vmlinux")
		if not os.path.exists(extract_script):
			await cls.download_file(
				"https://raw.githubusercontent.com/torvalds/linux/master/scripts/extract-vmlinux",
				extract_script,
			)
			os.chmod(extract_script, 0o700)

	@classmethod
	async def download_files(cls, release):
		version = UBUNTU_RELEASES.get(release)
		files = [
			(
				f"https://cloud-images.ubuntu.com/releases/{release}/release/ubuntu-{version}-server-cloudimg-amd64-root.tar.xz",
				f"{release}.root.tar.xz",
			),
			(
				f"https://cloud-images.ubuntu.com/releases/{release}/release/unpacked/ubuntu-{version}-server-cloudimg-amd64-initrd-generic",
				f"{release}.initrd",
			),
			(
				f"https://cloud-images.ubuntu.com/releases/{release}/release/unpacked/ubuntu-{version}-server-cloudimg-amd64-vmlinuz-generic",
				f"{release}.vmlinuz",
			),
		]
		for url, filename in files:
			file = os.path.join(CHROOT_PATH, ARTIFACTS_ROOT.lstrip("/"), filename)
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
	async def prepare_files(cls, release):
		await cls.extract_vmlinux(release)
		await cls.prepare_rootfs(release)

	@classmethod
	async def extract_vmlinux(cls, release):
		extract_script = os.path.join(ARTIFACTS_ROOT, "extract-vmlinux")
		vmlinuz_file = os.path.join(ARTIFACTS_ROOT, f"{release}.vmlinuz")
		kernel_file = os.path.join(CHROOT_PATH, ARTIFACTS_ROOT.lstrip("/"), f"{release}.kernel")
		await cls.run(f"{extract_script} {vmlinuz_file} > {kernel_file}", shell=True)

	@classmethod
	async def prepare_rootfs(cls, release):
		archive = os.path.join(ARTIFACTS_ROOT, f"{release}.root.tar.xz")
		rootfs = os.path.join(ARTIFACTS_ROOT, f"{release}.rootfs")

		await cls.run(f"truncate -s 2G {rootfs}")
		await cls.run(f"mkfs.ext4 -L 'cloudimg-rootfs' -F {rootfs}")

		with tempfile.TemporaryDirectory(
			prefix=f"{release}-rootfs-",
			dir=os.path.join(CHROOT_PATH, ARTIFACTS_ROOT.lstrip("/")),
			ignore_cleanup_errors=True,
		) as tempdir:
			temp = "/".join(tempdir.split("/")[2:])
			await cls.run(f"mount -o loop {rootfs} {temp}")
			await cls.run(f"tar -xf {archive} --directory {temp}")
			await cls.run(f"umount {temp}")
