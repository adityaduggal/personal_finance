// Copyright (c) 2020, Aditya Duggal and contributors
// For license information, please see license.txt

frappe.ui.form.on('Get Stock Price', {
	refresh: function(frm) {
        frm.disable_save();
	},
    onload: function(frm){
        cur_frm.cscript.set_item_query(frm)
	},
	type: function(frm){
	    cur_frm.cscript.set_item_query(frm)
	}
});


cur_frm.cscript.set_item_query = function(frm) {
    if (frm.doc.type === "Stock" || frm.doc.type === "Index"){
        var item_group = "Equity"
    } else if (frm.doc.type === "Mutual Fund"){
        var item_group = "Mutual Funds"
    } else {
        frappe.throw("No Implemented for {}".format(frm.doc.type))
    }
    frm.set_query("item_name", function(doc) {
        return {
            "filters": {
                "disabled": 0,
                "has_variants": 0,
                "item_group": item_group
            }
        };
    });
}