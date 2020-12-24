# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import time
import frappe
from ..doctype.get_stock_price.get_stock_price import update_all_prices


def update_pricing():
    st_time = time.time()
    it_list = frappe.db.sql("""SELECT name FROM `tabItem` WHERE docstatus=0 AND disabled=0""", as_dict=1)
    if it_list:
        for it in it_list:
            print(f"Processing {it.name}")
            update_all_prices(it.name)
    tot_time = int(time.time() - st_time)
    print(f"Total Time Taken {tot_time} seconds")
