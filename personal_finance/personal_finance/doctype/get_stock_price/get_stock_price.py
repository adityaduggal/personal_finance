# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import time
import frappe
from datetime import datetime
from frappe.utils import today, getdate
from frappe.model.document import Document
from ...api.mf_api.mf_api import get_mf_quote
from ..price_tracker.price_tracker import get_price_doc


class GetStockPrice(Document):
	def validate(self):
		if self.date:
			if getdate(self.date) >= getdate(today()):
				frappe.throw("Only Past Dates are Allowed")
		if self.item_name:
			itd = frappe.get_doc("Item", self.item_name)
			itgd = frappe.get_doc("Item Group", itd.item_group)
			if itgd.type_of_group == self.type:
				pass
			else:
				frappe.throw(f"{frappe.get_desk_link('Item', itd.name)} Selected is Not {self.type}.\nIt is "
							 f"{itgd.type_of_group} so Kindly Select {itgd.type_of_group} in Type Field.")
			if not itd.symbol:
				frappe.throw(f"{frappe.get_desk_link('Item', itd.name)} Does not have a Symbol Defined")
		else:
			frappe.throw("Please select an Equity to Get Prices")

	def get_prices(self):
		found = 0
		self.validate()
		itd = frappe.get_doc("Item", self.item_name)
		if self.type == "Mutual Fund":
			prices = get_mf_quote(itd.symbol)
			if prices.status == "SUCCESS":
				if self.date:
					for d in prices.data:
						d = frappe._dict(d)
						price_date = datetime.strptime(d.date, '%d-%m-%Y').date()
						if getdate(self.date) == price_date:
							found = 1
							frappe.msgprint(f"NAV= {d.nav} for Date= {self.date}")
							break
					if found != 1:
						frappe.msgprint(f"No NAV found for Date= {self.date}")
				else:
					frappe.msgprint("Date is Needed for Getting Price")
			else:
				frappe.throw("No Prices Received")


def update_all_prices(item_name):
	st_time = time.time()
	itd = frappe.get_doc("Item", item_name)
	itgd = frappe.get_doc("Item Group", itd.item_group)
	if itgd.type_of_group == "Mutual Fund" and itd.symbol:
		prices = get_mf_quote(itd.symbol)
		if prices.status == "SUCCESS":
			count = 0
			for d in prices.data:
				d = frappe._dict(d)
				price_date = getdate(d.date)
				price_doc = get_price_doc(itd.name, price_date)
				if price_doc:
					# Check if the price is empty then update else pass
					if price_doc.price == 0 and d.nav != price_doc.price:
						count += 1
						price_doc.price = d.nav
						try:
							price_doc.save()
						except:
							print(f"Some Error for {item_name} While Saving {price_doc.name}")
				else:
					count += 1
					ptr = frappe.new_doc("Price Tracker")
					ptr.investment = itd.name
					ptr.price = d.nav
					ptr.price_date = price_date
					ptr.save()
				if count > 0 and count % 1000 == 0:
					elapsed_time = int(time.time() - st_time)
					frappe.db.commit()
					print(f"Committing Changes After {count} Entries")
					print(f"Elapsed Time {elapsed_time} seconds")
		else:
			frappe.throw("No Prices Received")
	tot_time = int(time.time() - st_time)
	print(f"Total Time Taken {tot_time} seconds for {item_name}")
