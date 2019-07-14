# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

def validate(doc, method):
	if doc.linked_portfolio:
		port_acc = frappe.get_value("Portfolio", doc.linked_portfolio, "account")
		doc.account = port_acc
		if doc.account != port_acc:
			frappe.throw("Portfolio Account and Warehouse Account Should be Same for {}".format(doc.name))
	wh_list = frappe.db.sql("""SELECT name FROM `tabWarehouse` 
		WHERE disabled = 0 AND linked_portfolio IS NOT NULL AND name <> '%s'"""%(doc.name), as_list=1)
	for wh in wh_list:
		wh_doc = frappe.get_doc("Warehouse", wh[0])
		if wh_doc.linked_portfolio == doc.linked_portfolio:
			frappe.throw("Warehouse {} is already linked to Portfolio {}".format(wh[0], doc.linked_portfolio))