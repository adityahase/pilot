# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe

PROVIDER = "do"
DO_ACCESS_TOKEN = ""
CIDR = "10.10.0.0/24"
REGION = "blr1"
TITLE = "Bangalore"
NAME = "do-bangalore-blr1"


def create():
	if frappe.db.exists("Region", NAME):
		region = frappe.get_doc("Region", NAME)
	else:
		region = frappe.new_doc(
			"Region",
			**{
				"name": NAME,
				"access_token": DO_ACCESS_TOKEN,
				"cloud_provider": PROVIDER,
				"region_slug": REGION,
				"title": TITLE,
				"vpc_cidr_block": CIDR,
			},
		).insert()

	region.provision()


def destroy():
	if frappe.db.exists("Region", NAME):
		region = frappe.get_doc("Region", NAME)
		region.destroy()


def clear():
	doctypes = ["Provision Declaration", "Provision Plan", "Provision State", "Provision Action"]
	for doctype in doctypes:
		frappe.db.delete(doctype)
