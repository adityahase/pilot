// Copyright (c) 2025, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Node", {
	refresh(frm) {
		const actions = [
			[__("Ping"), "ping", false],
			[__("Setup"), "setup", true],
			[__("Update Agent"), "update_agent", true],
		];

		for (const [label, method, confirm] of actions) {
			// eslint-disable-next-line no-inner-declarations
			async function callback() {
				if (confirm && !(await frappe_confirm(label))) {
					return;
				}
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

async function frappe_confirm(label) {
	return new Promise((r) => {
		frappe.confirm(
			`Are you sure you want to ${label.toLowerCase()}?`,
			() => r(true),
			() => r(false)
		);
	});
}
