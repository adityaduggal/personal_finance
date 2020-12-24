# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from nsetools import Nse


def get_code_list(type):
    nse = Nse()
    if type == "Stock":
        return nse.get_stock_codes()
    elif type == "Index":
        return nse.get_index_list()
