# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class PriceTracker(Document):
    pass


def get_price_doc(item, date):
    price = []
    itd = frappe.get_doc("Item", item)
    itgd = frappe.get_doc("Item Group", itd.item_group)
    if itgd.type_of_group == "Mutual Fund":
        price_list = frappe.db.sql("""SELECT name FROM `tabPrice Tracker` WHERE investment = '%s' AND price_date = '%s'"""
                              % (item, date), as_dict=1)
        if price_list:
            price = frappe.get_doc("Price Tracker", price_list[0].name)

    return price
