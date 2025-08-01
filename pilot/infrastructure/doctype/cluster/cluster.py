# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

import ipaddress

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
		network = ipaddress.IPv4Network(self.cidr_block)
		self.gateway = f"{network[1]!s}/{network.prefixlen}"
		self.network_namespace = f"vpc-{cluster_count}"
