# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Region(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		access_token: DF.Password | None
		cloud_provider: DF.Link
		status: DF.Literal["Draft", "Pending", "Active", "Archived"]
		title: DF.Data
		vpc_cidr_block: DF.Data | None
		vpc_id: DF.Data | None
	# end: auto-generated types

	pass
