# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from pilot.infrastructure.ansible import Ansible


class Node(Document):
	@frappe.whitelist()
	def ping(self):
		self.ansible("ping.yml").run()

	@frappe.whitelist()
	def setup(self):
		self.ansible("node.yml", variables={"node": self.as_dict()}).run()

	def ansible(self, playbook, variables=None):
		return Ansible(self, playbook=playbook, variables=variables)
