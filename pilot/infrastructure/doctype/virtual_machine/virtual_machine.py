# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import frappe
import yaml
from frappe.model.document import Document

from pilot.agent import Agent


class VirtualMachine(Document):
	def before_insert(self):
		self.set_mac_address()
		self.set_tap_device()

	def after_insert(self):
		self.set_meta_data()
		self.set_user_data()
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
			},
			"resources": {
				"vcpu": self.vcpu,
				"memory": self.memory,
				"disk": self.disk,
			},
			"network": {
				"tap_device": self.tap_device,
				"mac_address": self.mac_address,
				"ip_address": self.ip_address,
				"gateway": self.gateway or "10.0.0.1",
				"subnet_mask": self.subnet_mask or "255.255.255.0",
			},
		}

	@property
	def agent(self):
		return Agent("localhost:8000")  # TODO: Replace with Node ip or hostname

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

	def set_mac_address(self):
		decimals = self.ip_address.split(".")
		hexes = [f"{int(d):02x}" for d in decimals]
		self.mac_address = "6e:fc:" + ":".join(hexes)
