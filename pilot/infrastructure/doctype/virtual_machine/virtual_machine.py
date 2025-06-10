# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import frappe
import yaml
from frappe.model.document import Document

from pilot.agent import Agent


class VirtualMachine(Document):
	def after_insert(self):
		self.set_metadata()
		self.save()

	def set_metadata(self):
		metadata = {
			"local-hostname": self.hostname,
			"instance-id": self.name,
		}
		self.metadata = yaml.dump(metadata)
		self.save()

	@frappe.whitelist()
	def provision(self):
		self.create_machine()

	@frappe.whitelist()
	def stop(self):
		self.agent.stop_machine(self.name)

	@frappe.whitelist()
	def terminate(self):
		self.agent.terminate_machine(self.name)

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
			"metadata": self.metadata,
			"resources": {
				"vcpu": self.vcpu,
				"memory": self.memory,
				"disk": self.disk,
			},
			"network": {
				"tap_device": self.tap_device or "tap0",
				"mac_address": self.mac_address or "00:00:00:00:00:01",
				"ip_address": self.ip_address or "10.0.0.100",
				"gateway": self.gateway or "10.0.0.1",
				"subnet_mask": self.subnet_mask or "255.255.255.0",
			},
		}

	@property
	def agent(self):
		return Agent("localhost:8000")  # TODO: Replace with Node ip or hostname
