import frappe

NODES = [
	{
		"name": "b1.metal.frappe.dev",
		"private_ip_address": "10.1.0.11",
		"public_ip_address": "62.210.158.82",
		"private_mac_address": "fake_mac",
		"private_vlan_id": "2081",
		"status": "Active",
	},
	{
		"name": "b2.metal.frappe.dev",
		"private_ip_address": "10.1.0.12",
		"public_ip_address": "62.210.158.140",
		"private_mac_address": "fake_mac",
		"private_vlan_id": "1863",
		"status": "Active",
	},
	{
		"name": "b3.metal.frappe.dev",
		"private_ip_address": "10.1.0.13",
		"public_ip_address": "62.210.158.144",
		"private_mac_address": "fake_mac",
		"private_vlan_id": "2081",
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
