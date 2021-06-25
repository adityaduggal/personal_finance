# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from nsetools import Nse
from nsepy import get_history
nse = Nse()


def get_code_list(type):
    if type == "Stock":
        return nse.get_stock_codes()
    elif type == "Index":
        return nse.get_index_list()


def get_stock_quote(stock, frm_dt, to_dt):
    q = get_history(symbol=stock, start=frm_dt, end=to_dt)
    q = q.fillna(0)
    return q
