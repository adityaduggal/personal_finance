// Copyright (c) 2016, Aditya Duggal and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Price Analysis"] = {
	"filters": [
		{
			"fieldname":"investment",
			"label": "Investment Name",
			"fieldtype": "Link",
			"options": "Item",
			"reqd": 1
		},
		{
			"fieldname":"sma1",
			"label": "SMA1-Period",
			"fieldtype": "Int",
			"default": 20,
			"reqd": 1
		},
		{
			"fieldname":"sma2",
			"label": "SMA2-Period",
			"fieldtype": "Int",
			"default": 200,
			"reqd": 1
		},
		{
			"fieldname":"ema1",
			"label": "EMA-Period",
			"fieldtype": "Int",
			"default": 10,
			"reqd": 1
		}
	]
};
