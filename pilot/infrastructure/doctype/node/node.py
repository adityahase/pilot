# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from pilot.infrastructure.ansible import Ansible


class Node(Document):
	@frappe.whitelist()
	def ping(self):
		Ansible(
			playbook="ping.yml",
			node=self,
			user="ubuntu",
			port="22",
		).run()
