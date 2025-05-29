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


def setup():
	for node in NODES:
		document = frappe.new_doc("Node")
		for key, value in node.items():
			document.set(key, value)
		document.insert()
