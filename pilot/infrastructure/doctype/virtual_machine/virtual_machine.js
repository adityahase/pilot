// Copyright (c) 2025, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Virtual Machine", {
	refresh(frm) {
		const actions = [
			[__("Provision"), "provision"],
			[__("Stop"), "stop", true],
			[__("Terminate"), "terminate", true],
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
			`Are you sure you want to ${label.toLowerCase()} this virtual machine?`,
			() => r(true),
			() => r(false)
		);
	});
}
