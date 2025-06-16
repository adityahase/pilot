# Copyright (c) 2025, Frappe and contributors
# For license information, please see license.txt

from subprocess import run

import frappe
from frappe.model.document import Document


class PilotSettings(Document):
	def validate(self):
		if not self.wireguard_private_key or not self.wireguard_public_key:
			self.generate_wireguard_keys()

	def generate_wireguard_keys(self):
		self.wireguard_private_key = self.generate_wireguard_private_key()
		self.wireguard_public_key = self.generate_wireguard_public_key()

	def generate_wireguard_private_key(self):
		return run(["wg", "genkey"], capture_output=True).stdout.decode().strip()

	def generate_wireguard_public_key(self):
		return (
			run(["wg", "pubkey"], input=self.wireguard_private_key.encode(), capture_output=True)
			.stdout.decode()
			.strip()
		)

	@frappe.whitelist()
	def get_wireguard_config(self):
		frappe.only_for("System Manager")
		nodes = frappe.get_all(
			"Node",
			fields=["name", "wireguard_public_key", "wireguard_ip_address", "public_ip_address"],
			filters={
				"status": "Active",
				"wireguard_public_key": ["is", "set"],
				"wireguard_ip_address": ["is", "set"],
				"public_ip_address": ["is", "set"],
			},
			order_by="name asc",
		)
		context = {
			"pilot": {
				"wireguard_private_key": self.get_password("wireguard_private_key"),
				"wireguard_ip_address": self.wireguard_ip_address,
			},
			"nodes": nodes,
		}
		return frappe.render_template(WIREGUARD_CONFIG_TEMPLATE, context)


WIREGUARD_CONFIG_TEMPLATE = """
[Interface]
PrivateKey = {{ pilot.wireguard_private_key }}
Address = {{ pilot.wireguard_ip_address }}/24
ListenPort = 51820

{% for node in nodes %}
[Peer] # {{ node.name }}
PublicKey = {{ node.wireguard_public_key }}
AllowedIPs = {{ node.wireguard_ip_address }}/32
Endpoint = {{ node.public_ip_address }}:51820
{% endfor %}
"""
