# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import flt

class IncomeExpenseEntry(Document):
	def validate(self):
		self.validate_account()

	def validate_account(self):
		for row in self.entries:
			if row.amount < 0:
				frappe.throw("Negative amount not allowed in Row# {}".format(row.idx))
			acct_doc = frappe.get_doc("Account", row.account)
			if acct_doc.root_type in ['Expense', 'Income']:
				if acct_doc.root_type != row.type_of_entry:
					frappe.throw("Selected Type of Entry is {} but Account {} is a {} type of Account in \
						Row# {}".format(row.type_of_entry, row.account, acct_doc.root_type, row.idx))
			if acct_doc.root_type in ['Asset', 'Liability']:
				if row.type_of_entry not in ['Transfer In', 'Transfer Out']:
					frappe.throw("Select type of Entry as Transfer for Account {} in \
						Row# {}".format(row.account, row.idx))
	def on_submit(self):
		self.post_jv_entries()
		jv_entries = self.get_existing_jv()
		if jv_entries:
			for jv in jv_entries:
				jv_doc = frappe.get_doc("Journal Entry", jv[0])
				jv_doc.submit()

	def on_cancel(self):
		jv_entries = self.get_existing_jv()
		if jv_entries:
			for jv in jv_entries:
				jv_doc = frappe.get_doc("Journal Entry", jv[0])
				jv_doc.cancel()

	def post_jv_entries(self):
		global_defaults = frappe.get_single("Global Defaults")
		for row in self.entries:
			jv_dict = {}
			jv_map = []
			if row.type_of_entry in ["Expense", "Transfer Out"]:
				debit_amt = flt(row.amount)
				credit_amt = 0
			elif row.type_of_entry in ["Income", "Transfer In"]:
				credit_amt = flt(row.amount)
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
			})
			jv_map.append(jv_dict)
			jv_dict = frappe._dict({
				'company': global_defaults.default_company,
				'posting_date' : row.date,
				'voucher_type': self.doctype,
				'voucher_no': self.name,
				'account': row.account,
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
					"user_remark": self.doctype + " " + row.type_of_entry + " for " \
						+ row.description + " for Row #" + str(row.idx),
					"accounts": jv_map
					})
			jv.insert()

	def get_existing_jv(self):
		chk_jv = frappe.db.sql("""SELECT name FROM `tabJournal Entry`
			WHERE docstatus != 2 AND
			linked_doctype = '%s' AND linked_document = '%s'"""% (self.doctype, self.name), as_list=1)
		return chk_jv