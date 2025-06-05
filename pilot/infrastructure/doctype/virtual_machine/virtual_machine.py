# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

# import frappe
from pprint import pprint

from frappe.model.document import Document

from pilot.agent import Agent


class VirtualMachine(Document):
	def after_insert(self):
		agent = Agent("localhost:8000")  # TODO: Replace with Node ip or hostname
		machine = self.get_machine_details()
		agent.create_machine(machine)

	def get_machine_details(self):
		return {
			"name": self.name,
			"hostname": self.hostname,
			"boot": {
				"kernel": self.kernel,
				"root_filesystem": self.root_filesystem,
				"initial_ram_disk": self.initial_ram_disk,
			},
			"resources": {
				"vcpu": self.vcpu,
				"memory": self.memory,
				"disk": self.disk,
			},
			"network": {
				"tap_device": self.tap_device or "tap1",
				"mac_address": self.mac_address or "00:00:00:00:00:01",
				"ip_address": self.ip_address or "10.0.0.100",
				"gateway": self.gateway or "10.0.0.1",
				"subnet_mask": self.subnet_mask or "255.255.255.0",
			},
		}
