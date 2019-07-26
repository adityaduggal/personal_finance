// Copyright (c) 2016, Aditya Duggal and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Portfolio Status"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": "Date",
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"portfolio",
			"label": "Portfolio",
			"fieldtype": "Link",
			"options": "Portfolio"
		},
		{
			"fieldname":"investment",
			"label": "Investment Name",
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname":"zero",
			"label": "Show Zero Investments",
			"fieldtype": "Check",
			"default": 0
		},
	]
}
