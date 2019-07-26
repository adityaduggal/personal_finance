// Copyright (c) 2016, Aditya Duggal and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Portfolio Transactions"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -12),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": "To Date",
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
			"fieldname":"account",
			"label": "Account",
			"fieldtype": "Link",
			"options": "Account"
		},
		{
			"fieldname":"investment",
			"label": "Investment Name",
			"fieldtype": "Link",
			"options": "Item"
		},
	]
}