# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AnsiblePlay(Document):
	def on_trash(self):
		if frappe.conf.developer_mode:
			tasks = frappe.get_all("Ansible Task", filters={"play": self.name}, pluck="name")
			for task in tasks:
				frappe.delete_doc("Ansible Task", task)
