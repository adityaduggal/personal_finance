// Copyright (c) 2019, Aditya Duggal and contributors
// For license information, please see license.txt

frappe.ui.form.on('Investment Transaction', {
	refresh: function(frm) {

	}
});

frappe.ui.form.on('Investment Transaction Detail', "quantity", function(frm, cdt, cdn){
	var d = locals[cdt][cdn]
	frappe.model.set_value(cdt, cdn, "total", (d.quantity * d.price) + d.commission);	
	cur_frm.refresh_fields();
});
frappe.ui.form.on('Investment Transaction Detail', "price", function(frm, cdt, cdn){
	var d = locals[cdt][cdn]
	frappe.model.set_value(cdt, cdn, "total", (d.quantity * d.price) + d.commission);	
	cur_frm.refresh_fields();
});
frappe.ui.form.on('Investment Transaction Detail', "commission", function(frm, cdt, cdn){
	var d = locals[cdt][cdn]
	frappe.model.set_value(cdt, cdn, "total", (d.quantity * d.price) + d.commission);	
	cur_frm.refresh_fields();
});