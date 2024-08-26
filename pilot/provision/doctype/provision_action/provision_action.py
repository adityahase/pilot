# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ProvisionAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action: DF.Data
		error: DF.Code | None
		name: DF.Int | None
		output: DF.Code | None
		parsed_output: DF.Code | None
		region: DF.Link
		stack: DF.Data
	# end: auto-generated types

	pass
