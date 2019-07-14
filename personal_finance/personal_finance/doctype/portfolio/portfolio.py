# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Portfolio(Document):
	def validate(self):
		linked_acc_type = frappe.get_value("Account", self.account, "account_type")
		if linked_acc_type != "Stock":
			frappe.throw("Portfolio Account should be Stock Type only")
		self.portfolio_linked_warehouse(err_msg=0)

	def portfolio_linked_warehouse(self, err_msg):
		wh_list = frappe.db.sql("""SELECT name FROM `tabWarehouse` 
			WHERE disabled=0 AND linked_portfolio='%s'"""%(self.name),as_list=1)
		if len(wh_list)>1:
			frappe.throw("More than 2 warehouses linked to Porfolio {}".format(self.name))
		if len(wh_list)==0:
			if err_msg == 0:
				frappe.msgprint("Please link Portfolio: {} with One Warehouse to do any transactions".format(self.name))
			else:
				frappe.throw("Please link Portfolio: {} with One Warehouse to do any transactions".format(self.name))
		if len(wh_list)==1:
			wh_doc = frappe.get_doc("Warehouse", wh_list[0][0])
			if wh_doc.account != self.account:
				wh_doc.account = self.account
				wh_doc.save()