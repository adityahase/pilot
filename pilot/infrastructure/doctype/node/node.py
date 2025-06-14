# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import ipaddress

import frappe
from frappe.model.document import Document

from pilot.infrastructure.ansible import Ansible


class Node(Document):
	def before_insert(self):
		self.multicast_address = str(ipaddress.IPv4Network(self.multicast_cidr_block)[1])

	@frappe.whitelist()
	def ping(self):
		self.ansible("ping.yml").run()

	@frappe.whitelist()
	def setup(self):
		self.ansible("node.yml", variables={"node": self.as_dict()}).run()

	@frappe.whitelist()
	def update_agent(self):
		self.ansible("agent.yml").run()

	def ansible(self, playbook, variables=None):
		return Ansible(self, playbook=playbook, user=self.ssh_user, variables=variables)

	def on_trash(self):
		if frappe.conf.developer_mode:
			self._delete_plays()
			self._delete_virtual_machines()

	def _delete_plays(self):
		plays = frappe.get_all("Ansible Play", filters={"node": self.name}, pluck="name")
		for play in plays:
			frappe.delete_doc("Ansible Play", play)

	def _delete_virtual_machines(self):
		machines = frappe.get_all("Virtual Machine", filters={"node": self.name}, pluck="name")
		for machine in machines:
			frappe.delete_doc("Virtual Machine", machine)
