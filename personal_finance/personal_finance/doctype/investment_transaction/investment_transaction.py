# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt, formatdate, getdate
from erpnext.accounts.general_ledger import make_gl_entries, delete_gl_entries
from erpnext.stock.utils import get_bin
from erpnext.accounts.utils import get_fiscal_year
import datetime

class InvestmentTransaction(Document):
	def validate(self):
		self.validate_negative_balance()

	def on_submit(self):
		self.make_price_tracker(flag='create')
		self.post_jv_entries()
		self.post_ste()
		chk_ste = self.get_existing_ste()
		chk_jv = self.get_existing_jv()
		if chk_jv:
			for jv in chk_jv:
				jv_doc = frappe.get_doc("Journal Entry", jv[0])
				jv_doc.submit()
		if chk_ste:
			for ste in chk_ste:
				ste_doc = frappe.get_doc("Stock Entry", ste[0])
				ste_doc.submit()

	def on_cancel(self):
		self.make_price_tracker(flag='delete')
		delete_gl_entries(None, self.doctype, self.name)
		self.cancel_ste()
		self.cancel_jv()

	def validate_negative_balance(self):
		for row in self.transactions:
			if row.type_of_transaction == "Dividend":
				if row.quantity > 0:
					frappe.throw("For dividend Quantity has to be ZERO for Row# {}".format(row.idx))
			if row.type_of_transaction == "Split":
				if row.total > 0:
					frappe.throw("For Split Transactions Total amount has to be ZERO for Row# {}".format(row.idx))
			row.total = (row.quantity * row.price) + row.commission
			if row.quantity < 0:
				frappe.throw("Negative Quantity is not allowed. Check Row# {}".format(row.idx))
			if row.price < 0:
				frappe.throw("Negative Price is not allowed. Check Row# {}".format(row.idx))
			if row.commission < 0:
				frappe.throw("Negative Commission is not allowed. Check Row# {}".format(row.idx))
			if row.total < 0:
				frappe.throw("Negative Total is not allowed. Check Row# {}".format(row.idx))

	def post_jv_entries(self):
		jv_map = []
		global_defaults = frappe.get_single("Global Defaults")
		investment_account = frappe.get_value("Portfolio", self.portfolio, "account")
		gain_loss_account = frappe.get_value("Portfolio", self.portfolio, "loss_gain_account")

		for row in self.transactions:
			if row.type_of_transaction in ["Dividend", "Split"]:
				jv_dict = {}
				jv_map = []
				if row.type_of_transaction == "Split":
					debit_amt = 0
					credit_amt = flt(row.quantity)
				elif row.type_of_transaction == "Dividend":
					credit_amt = flt(row.total)
					debit_amt = 0

				jv_dict = frappe._dict({
					'company': global_defaults.default_company,
					'posting_date' : row.date,
					'voucher_type': self.doctype,
					'voucher_no': self.name,
					'account': self.account,
					'debit': credit_amt,
					'debit_in_account_currency' : credit_amt,
					'credit_in_account_currency': debit_amt,
					'credit': debit_amt,
					'party_type': 'Item',
					'party': row.investment_name,
					'remarks': row.type_of_transaction + " " + row.investment_name + " Qty:" + str(row.quantity) + " @" + str(row.price)
				})
				jv_map.append(jv_dict)
				jv_dict = frappe._dict({
					'company': global_defaults.default_company,
					'posting_date' : row.date,
					'voucher_type': self.doctype,
					'voucher_no': self.name,
					'account': gain_loss_account,
					'debit': debit_amt,
					'debit_in_account_currency' : debit_amt,
					'credit_in_account_currency': credit_amt,
					'credit': credit_amt
				})
				jv_map.append(jv_dict)
				jv = frappe.get_doc({
						"doctype": "Journal Entry",
						"linked_doctype": self.doctype,
						"linked_document": self.name,
						"voucher_type": "Journal Entry",
						#"set_posting_time": 1,
						"posting_date": row.date,
						#"posting_time": time,
						"user_remark": "Investment Transaction " + row.type_of_transaction + " of Item: " \
							+ row.investment_name + " for Row #" + str(row.idx),
						"accounts": jv_map
						})
				jv.insert()

	def post_ste(self):
		port_doc = frappe.get_doc("Portfolio", self.portfolio)
		investment_account = frappe.get_value("Portfolio", self.portfolio, "account")
		gain_loss_account = frappe.get_value("Portfolio", self.portfolio, "loss_gain_account")
		wh_list = frappe.db.sql("""SELECT name FROM `tabWarehouse` 
			WHERE linked_portfolio = '%s' """%(self.portfolio), as_list=1)
		if not wh_list:
			frappe.throw("Portfolio {} is not linked to any Warehouse".format(self.portfolio))
		if len(wh_list) > 1:
			frappe.throw("Portfolio {} is linked to more than 1 Warehouse".format(self.portfolio))
		for row in self.transactions:
			ste_items = []
			ste_temp = {}
			if row.type_of_transaction in ["Buy", "Sell", "Split"]:
				if row.type_of_transaction == "Buy":
					ste_temp.setdefault("t_warehouse", wh_list[0][0])
					ste_temp.setdefault("expense_account", self.account)
					purpose = "Material Receipt"
					time = "00:00:01"
				elif row.type_of_transaction == "Sell":
					ste_temp.setdefault("s_warehouse", wh_list[0][0])
					ste_temp.setdefault("expense_account", self.account)
					purpose = "Material Issue"
					time = "23:59:59"
				elif row.type_of_transaction == "Split":
					ste_temp.setdefault("t_warehouse", wh_list[0][0])
					ste_temp.setdefault("expense_account", self.account)
					purpose = "Material Receipt"
					time = "00:00:01"

				ste_temp.setdefault("item_code", row.investment_name)
				ste_temp.setdefault("qty", row.quantity)
				if (row.total/row.quantity) > 0:
					ste_temp.setdefault("basic_rate", (row.total/row.quantity))
				else:
					ste_temp.setdefault("basic_rate", 1)
				ste_items.append(ste_temp)
				ste = frappe.get_doc({
						"doctype": "Stock Entry",
						"linked_doctype": self.doctype,
						"linked_document": self.name,
						"purpose": purpose,
						"set_posting_time": 1,
						"posting_date": row.date,
						"posting_time": time,
						"remarks": "Investment Transaction " + row.type_of_transaction + " of Item: " \
							+ row.investment_name + " for Row #" + str(row.idx),
						"items": ste_items
						})
				ste.insert()

	def cancel_jv(self):
		chk_jv = self.get_existing_jv()
		if chk_jv:
			for jv in chk_jv:
				jv_doc = frappe.get_doc("Journal Entry", jv[0])
				jv_doc.cancel()

	def cancel_ste(self):
		chk_ste = self.get_existing_ste()
		if chk_ste:
			for ste in chk_ste:
				ste_doc = frappe.get_doc("Stock Entry", ste[0])
				ste_doc.cancel()

	def get_existing_ste(self):
		chk_ste = frappe.db.sql("""SELECT ste.name FROM `tabStock Entry` ste
			WHERE ste.docstatus != 2 AND
			ste.linked_doctype = '%s' AND ste.linked_document = '%s'"""% (self.doctype, self.name), as_list=1)
		return chk_ste

	def get_existing_jv(self):
		chk_jv = frappe.db.sql("""SELECT name FROM `tabJournal Entry`
			WHERE docstatus != 2 AND
			linked_doctype = '%s' AND linked_document = '%s'"""% (self.doctype, self.name), as_list=1)
		return chk_jv

	def make_price_tracker(self, flag=None):
		for row in self.transactions:
			if row.type_of_transaction == 'Buy' or 'Sell':
				ptracker = frappe.db.sql("""SELECT name FROM `tabPrice Tracker` 
					WHERE investment = '%s' AND price_date = '%s'"""%(row.investment_name, row.date), as_list=1)
				if not ptracker and flag == 'create':
					pt_doc = frappe.new_doc("Price Tracker")
					pt_doc.investment = row.investment_name
					pt_doc.price_date = row.date
					pt_doc.price = row.price
					pt_doc.insert()
				if flag == 'delete' and ptracker:
					pt_doc = frappe.get_doc('Price Tracker', ptracker[0][0])
					pt_doc.delete()