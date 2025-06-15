# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import ipaddress
import random

import frappe
import yaml
from frappe.model.document import Document

from pilot.agent import Agent


class VirtualMachine(Document):
	def before_insert(self):
		self.set_ip_address()
		self.set_mac_address()
		self.set_tap_device()
		self.set_user_identifiers()

	def after_insert(self):
		self.set_meta_data()
		self.set_user_data()
		self.set_network_config()
		self.save()

	@frappe.whitelist()
	def provision(self):
		self.create_machine()
		self.status = "Running"
		self.save()

	@frappe.whitelist()
	def stop(self):
		self.agent.stop_machine(self.name)
		self.status = "Stopped"
		self.save()

	@frappe.whitelist()
	def terminate(self):
		self.agent.terminate_machine(self.name)
		self.status = "Terminated"
		self.save()

	def create_machine(self):
		machine = self.get_machine_details()
		self.agent.create_machine(machine)

	def get_machine_details(self):
		return {
			"name": self.name,
			"hostname": self.hostname,
			"boot": {
				"kernel": self.kernel,
				"root_filesystem": self.root_filesystem,
				"initial_ram_disk": self.initial_ram_disk,
			},
			"meta-data": {
				"meta-data": self.meta_data,
				"user-data": self.user_data,
				"network-config": self.network_config,
			},
			"resources": {
				"vcpu": self.vcpu,
				"memory": self.memory,
				"disk": self.disk,
			},
			"network": {
				"cluster": self.get_cluster_details(),
				"tap_device": self.tap_device,
				"mac_address": self.mac_address,
				"ip_address": self.ip_address,
				"gateway": self.gateway,
				"subnet_mask": self.subnet_mask,
			},
			"isolation": {
				"user_id": self.user_id,
				"group_id": self.group_id,
			},
		}

	@property
	def agent(self):
		index = int(self.node.split(".")[0][-1])
		return Agent(f"localhost:{18000 + index}")  # TODO: Replace with Node ip or hostname

	def set_meta_data(self):
		meta_data = {
			"local-hostname": self.hostname,
			"instance-id": self.name,
		}
		self.meta_data = yaml.dump(meta_data)

	def set_user_data(self):
		if self.ssh_key:
			ssh_public_key = frappe.db.get_value("SSH Key", self.ssh_key, "public_key")
			user_data = {"users": [{"name": "root", "ssh_authorized_keys": [ssh_public_key]}]}
			formatted_user_data = yaml.dump(user_data)

		else:
			formatted_user_data = ""
		self.user_data = f"#cloud-config\n{formatted_user_data}"

	def set_tap_device(self):
		if not self.tap_device:
			machines = frappe.db.count(
				"Virtual Machine",
				{"status": ("!=", "Terminated"), "node": self.node},
			)
			self.tap_device = f"tap{machines}"

	def set_ip_address(self):
		network = ipaddress.IPv4Network(self.subnet_cidr_block)
		self.gateway = str(network[1])
		self.subnet_mask = str(network.netmask)
		if not self.ip_address:
			machines = frappe.db.count(
				"Virtual Machine",
				{"status": ("!=", "Terminated"), "node": self.node},
			)

			# Skip the first two addresses in the network.
			# First is the Network address.
			# Second is the gateway address.
			index = 2 + machines
			self.ip_address = str(network[index])

	def set_mac_address(self):
		decimals = self.ip_address.split(".")
		hexes = [f"{int(d):02x}" for d in decimals]
		self.mac_address = "6e:fc:" + ":".join(hexes)

	def set_user_identifiers(self):
		if not self.user_id or not self.group_id:
			self.user_id = random.randint(1_000_000_000, 2_000_000_000)
			self.group_id = self.user_id

	def set_network_config(self):
		"""
		Sets the network configuration for the virtual machine.
		This is used in the user data for cloud-init.
		"""
		network = ipaddress.IPv4Network(self.subnet_cidr_block)
		network_config = {
			"network": {
				"version": 2,
				"ethernets": {
					"eth0": {
						"match": {"macaddress": self.mac_address},
						"addresses": [f"{self.ip_address}/{network.prefixlen}"],
						"routes": [{"to": "default", "via": self.gateway}],
						"nameservers": {"addresses": ["8.8.8.8", "8.8.4.4"]},
						"dhcp4": False,
						"dhcp6": False,
					}
				},
			}
		}
		network_config = yaml.dump(network_config)
		self.network_config = f"#cloud-config\n{network_config}"

	def get_cluster_details(self):
		cluster = frappe.get_doc("Cluster", self.cluster)
		node = frappe.get_doc("Node", self.node)
		return {
			"gateway": cluster.gateway,
			"bridge": cluster.bridge,
			"vxlan": cluster.vxlan,
			"vni": cluster.vni,
			"multicast_address": node.multicast_address,
			"private_interface": node.private_interface,
			"public_interface": node.public_interface,
		}
