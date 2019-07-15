# -*- coding: utf-8 -*-
# Copyright (c) 2019, Rohit Industries Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute():
	delete_cancelled_docs()

def delete_cancelled_docs():
	dt_list = ["Journal Entry", "Stock Entry", "Investment Transaction"]
	deleted_doc = ["Price Tracker", "Journal Entry", "Stock Entry", "Investment Transaction"]
	for dt in dt_list:
		linked_docs = frappe.db.sql("""SELECT amended_from FROM `tab%s` 
			WHERE docstatus !=2 AND amended_from IS NOT NULL"""%(dt),as_list=1)
		cancelled_docs = frappe.db.sql("""SELECT name FROM `tab%s` WHERE docstatus=2 
			AND name NOT IN (SELECT amended_from FROM `tab%s` WHERE amended_from = name)"""%(dt, dt), as_list=1)
		if cancelled_docs:
			for c_docs in cancelled_docs:
				check = any (c_docs[0] in sublist for sublist in linked_docs)
				if check != 1:
					frappe.delete_doc_if_exists(dt, c_docs[0])
					print("Deleted " + dt + " with Name: " + c_docs[0])
	for doc in deleted_doc:
		print(doc)
		doc_list = frappe.db.sql("""SELECT name, deleted_doctype, deleted_name FROM `tabDeleted Document` 
			WHERE deleted_doctype = '%s' """%(doc),as_list=1)
		for dt_item in doc_list:
			print("Deleting Deleted Document: " + dt_item[0] + " for Doctype: " + dt_item[1] + \
				" with Document Number: " + dt_item[2])
			frappe.delete_doc_if_exists("Deleted Document", dt_item[0])