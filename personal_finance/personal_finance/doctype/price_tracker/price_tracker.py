# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import pandas as pd
from frappe.model.document import Document
from frappe.utils import getdate


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


def update_price_doc_values(price_doc, df):
    frappe.throw("Hello Update")



def create_new_stock_price(it_name, price_date, df):
    itd = frappe.get_doc("Item", it_name)
    pt = frappe.new_doc("Price Tracker")
    pt.investment = it_name
    pt.price_date = price_date
    pt.price = df["Close"]
    pt.open = df["Open"]
    pt.high = df["High"]
    pt.low = df["Low"]
    pt.close = df["Close"]
    pt.vwap = df["VWAP"]
    pt.volume = df["Volume"]
    pt.delivered_volume = df["Deliverable Volume"]
    itd.prices_fetched_upto = price_date
    pt.insert()
    print(f"Created {pt.name} for {it_name} for Date: {price_date}")



def update_stock_prices(it_name, pd_df):
    pd_df.fillna(0)
    dates = pd_df.index
    itd = frappe.get_doc("Item", it_name)
    for index, row in pd_df.iterrows():
        cur_date = getdate(index)
        price_doc = get_price_doc(it_name, getdate(index))
        if price_doc:
            update_price_doc_values(price_doc, row)
        else:
            create_new_stock_price(it_name, getdate(index), row)
    itd.prices_fetched_upto = cur_date
    itd.save()
