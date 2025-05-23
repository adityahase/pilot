// Copyright (c) 2025, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Node", {
	refresh(frm) {
		const ping_actions = [[__("Ping"), "ping"]];

		for (const [label, method] of ping_actions) {
			// eslint-disable-next-line no-inner-declarations
			async function callback() {
				const res = await frm.call(method);
				if (res.message) {
					frappe.msgprint(res.message);
				} else {
					frm.refresh();
				}
			}
			frm.add_custom_button(label, callback, __("Actions"));
		}
	},
});
