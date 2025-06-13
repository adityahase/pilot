import os

import frappe
import requests

NODES = [
	{
		"name": "b1.metal.frappe.dev",
		"private_ip_address": "10.1.0.11",
		"public_ip_address": "62.210.158.82",
		"private_mac_address": "fake_mac",
		"private_vlan_id": "2081",
		"public_interface": "enp65s0f0",
		"private_interface": " private",
		"private_vlan_link": "eth0",
		"ssh_user": "ubuntu",
		"status": "Active",
	},
	{
		"name": "b2.metal.frappe.dev",
		"private_ip_address": "10.1.0.12",
		"public_ip_address": "62.210.158.140",
		"private_mac_address": "fake_mac",
		"private_vlan_id": "1863",
		"public_interface": "enp65s0f0",
		"private_interface": "private",
		"private_vlan_link": "eth0",
		"ssh_user": "ubuntu",
		"status": "Active",
	},
	{
		"name": "b3.metal.frappe.dev",
		"private_ip_address": "10.1.0.13",
		"public_ip_address": "62.210.158.144",
		"private_mac_address": "fake_mac",
		"private_vlan_id": "2081",
		"public_interface": "enp65s0f0",
		"private_interface": "private",
		"private_vlan_link": "eth0",
		"ssh_user": "ubuntu",
		"status": "Active",
	},
	{
		"name": "d1.metal.frappe.dev",
		"private_ip_address": "10.139.248.160",
		"public_ip_address": "157.245.109.147",
		"private_mac_address": "fake_mac",
		"private_vlan_id": "fake_vlan_id",
		"public_interface": "eth0",
		"private_interface": "eth1",
		"private_vlan_link": "fake_vlan_link",
		"ssh_user": "root",
		"status": "Active",
	},
]

IMAGES = [
	{
		"name": "Ubuntu 20.04",
		"kernel": "focal.kernel",
		"initial_ram_disk": "focal.initrd",
		"root_filesystem": "focal.rootfs",
	},
	{
		"name": "Ubuntu 22.04",
		"kernel": "jammy.kernel",
		"initial_ram_disk": "jammy.initrd",
		"root_filesystem": "jammy.rootfs",
	},
	{
		"name": "Ubuntu 24.04",
		"kernel": "noble.kernel",
		"initial_ram_disk": "noble.initrd",
		"root_filesystem": "noble.rootfs",
	},
	{
		"name": "Ubuntu Firecracker 24.04",
		"kernel": "ubuntu-24.04-firecracker.kernel",
		"root_filesystem": "ubuntu-24.04-firecracker.rootfs",
	},
	{
		"name": "Ubuntu Firecracker 24.04 Linux 5.x",
		"kernel": "ubuntu-24.04-firecracker-linux-5.x.kernel",
		"root_filesystem": "ubuntu-24.04-firecracker.rootfs",
	},
]


def setup():
	for node in NODES:
		if frappe.db.exists("Node", node["name"]):
			continue
		document = frappe.new_doc("Node")
		for key, value in node.items():
			document.set(key, value)
		document.insert()

	for image in IMAGES:
		if frappe.db.exists("Image", image["name"]):
			continue
		document = frappe.new_doc("Image")
		for key, value in image.items():
			document.set(key, value)
		document.insert()


def cleanup():
	for node in NODES:
		if not frappe.db.exists("Node", node["name"]):
			continue
		frappe.delete_doc("Node", node["name"])


def install():
	SERVERS = {
		("b1.metal.frappe.dev", "fr-par-1", "232d8cc8-38d2-4791-8ac7-8747369e34d2"),
		("b2.metal.frappe.dev", "fr-par-1", "de0db1e3-8693-4ff0-899b-8f8c9d616aa6"),
		("b3.metal.frappe.dev", "fr-par-1", "db826636-1b20-45c1-a41e-e9e7039a4773"),
	}
	BOOT_SPACE = 536870912  # 512 MiB
	ROOT_SPACE = 21474836480  # 20 GiB
	SCW_SECRET_KEY = os.environ.get("SCW_SECRET_KEY")
	for name, zone, id in SERVERS:
		response = requests.post(
			f"https://api.scaleway.com/baremetal/v1/zones/{zone}/servers/{id}/install",
			headers={"X-Auth-Token": SCW_SECRET_KEY},
			json={
				"os_id": "7d1914e1-f4ab-47fc-bd8c-b3a23143e87a",
				"hostname": name,
				"ssh_key_ids": ["6b3dd40a-9d07-4ebc-9576-717973c1c52f"],
				"partitioning_schema": {
					"disks": [
						{
							"device": "/dev/nvme0n1",
							"partitions": [
								{
									"label": "uefi",
									"number": 1,
									"size": BOOT_SPACE,
									"use_all_available_space": False,
								},
								{
									"label": "boot",
									"number": 2,
									"size": BOOT_SPACE,
									"use_all_available_space": False,
								},
								{
									"label": "root",
									"number": 3,
									"size": ROOT_SPACE,
									"use_all_available_space": False,
								},
								{"label": "data", "number": 4, "use_all_available_space": True},
							],
						},
						{
							"device": "/dev/nvme1n1",
							"partitions": [
								{
									"label": "boot",
									"number": 1,
									"size": BOOT_SPACE,
									"use_all_available_space": False,
								},
								{
									"label": "root",
									"number": 2,
									"size": ROOT_SPACE,
									"use_all_available_space": False,
								},
								{"label": "data", "number": 3, "use_all_available_space": True},
							],
						},
					],
					"raids": [
						{
							"name": "/dev/md0",
							"level": "raid_level_1",
							"devices": ["/dev/nvme0n1p2", "/dev/nvme1n1p1"],
						},
						{
							"name": "/dev/md1",
							"level": "raid_level_1",
							"devices": ["/dev/nvme0n1p3", "/dev/nvme1n1p2"],
						},
					],
					"filesystems": [
						{"device": "/dev/nvme0n1p1", "format": "fat32", "mountpoint": "/boot/efi"},
						{"device": "/dev/md0", "format": "ext4", "mountpoint": "/boot"},
						{"device": "/dev/md1", "format": "ext4", "mountpoint": "/"},
						{"device": "/dev/nvme0n1p4", "format": "ext4", "mountpoint": "/data1"},
						{"device": "/dev/nvme1n1p3", "format": "ext4", "mountpoint": "/data2"},
					],
				},
			},
		)
		if response.status_code == 200:
			print(f"Install request for {name} accepted.")
		else:
			print(f"Failed to install {name}: {response.status_code} : {response.text}")
