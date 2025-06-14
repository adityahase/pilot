# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Cluster(Document):
	def before_insert(self):
		cluster_count = frappe.db.count(
			"Cluster",
		)
		self.vni = cluster_count
		self.vxlan = f"vxlan-{cluster_count}"
		self.bridge = f"br-{cluster_count}"
