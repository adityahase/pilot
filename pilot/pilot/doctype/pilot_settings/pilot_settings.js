// Copyright (c) 2025, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Pilot Settings", {
	refresh(frm) {
		frm.add_custom_button(
			"Get Wireguard Configuration",
			function () {
				frm.call("get_wireguard_config").then((r) => {
					frappe.msgprint({
						message: `<pre>${r.message}</pre>`,
						title: __("WireGuard Configuration"),
					});
				});
			},
			__("Actions")
		);
	},
});
