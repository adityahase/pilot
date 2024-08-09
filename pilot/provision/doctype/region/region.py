# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from pilot.provision.opentofu import OpenTofu


class Region(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		access_token: DF.Password | None
		cloud_provider: DF.Link
		region_slug: DF.Data
		status: DF.Literal["Draft", "Pending", "Active", "Archived"]
		title: DF.Data
		vpc_cidr_block: DF.Data | None
		vpc_id: DF.Data | None
	# end: auto-generated types

	@frappe.whitelist()
	def provision(self) -> None:
		OpenTofu(self).provision()

	@frappe.whitelist()
	def destroy(self) -> None:
		OpenTofu(self).destroy()

	def on_trash(self) -> None:
		zones = frappe.get_all("Zone", filters={"region": self.name})
		for zone in zones:
			frappe.delete_doc("Zone", zone.name)
