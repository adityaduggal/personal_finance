# Copyright (c) 2013, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	return ["Transaction #:Link/Investment Transaction:100", "Portfolio:Link/Portfolio:120", 
		"Account:Link/Account:180", "Type of Transaction::100", "Date:Date:80",
		"Investment:Link/Item:180", "Qty:Float:80", "Price:Currency:80",
		"Commission:Currency:80", "Total:Currency:100", "Remarks::250"]

def get_data(filters):
	data = []
	cond_it, cond_itd = get_conditions(filters)
	data = frappe.db.sql("""SELECT it.name, it.portfolio, it.account, itd.type_of_transaction,
		itd.date, itd.investment_name, itd.quantity, itd.price, itd.commission,
		itd.total, itd.remarks FROM `tabInvestment Transaction` it, `tabInvestment Transaction Detail` itd
		WHERE itd.docstatus = 1 AND itd.parent = it.name %s %s
		ORDER BY it.portfolio, it.account, itd.date"""%(cond_it, cond_itd),as_list=1)
	return data

def get_conditions(filters):
	cond_it = ""
	cond_itd = ""

	if filters.get("from_date"):
		cond_itd += " AND itd.date >= '%s'" % filters.get("from_date")

	if filters.get("to_date"):
		cond_itd += " AND itd.date <= '%s'" % filters.get("to_date")
	
	if filters.get("portfolio"):
		cond_itd += " AND it.portfolio = '%s'" % filters.get("portfolio")

	if filters.get("account"):
		cond_itd += " AND it.account = '%s'" % filters.get("account")

	if filters.get("investment"):
		cond_itd += " AND itd.investment_name = '%s'" % filters.get("investment")

	return cond_it, cond_itd