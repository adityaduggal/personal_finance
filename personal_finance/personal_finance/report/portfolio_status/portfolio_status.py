# Copyright (c) 2013, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, getdate, nowdate


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    return ["Portfolio:Link/Portfolio:120", "Investment Name:Link/Item:180", "Group::80", "Symbol::80",
            "Quantity:Float:80", "Cost Price:Currency:80", "Total Cost:Currency:120", "Realised P/L:Currency:120",
            "Unrealised P/L:Currency:120", "Dividend:Currency:80", "Total P/L:Currency:100", "ROI:Percent:80",
            "Annualised ROI:Percent:80", "Latest Date:Date:80", "Latest Price:Currency:80", "Latest Value:Currency:120"]


def get_data(filters):
    data = []
    row = []
    zero_invest = filters.get("zero")
    cond_it, cond_itd, cond_ptrack = get_conditions(filters)

    query = """SELECT it.name, it.portfolio, itd.date, itd.type_of_transaction, itd.investment_name,
    itd.quantity, itd.price, itd.commission, itd.total
    FROM `tabInvestment Transaction` it, `tabInvestment Transaction Detail` itd
    WHERE it.docstatus = 1 AND itd.parent = it.name %s %s
    ORDER BY itd.date""" % (cond_it, cond_itd)

    invst_tran = frappe.db.sql(query, as_dict=1)
    if not filters.get("Portfolio"):
        portfolio = frappe.db.sql("""SELECT name FROM `tabPortfolio` WHERE docstatus=0""", as_list=1)
    else:
        portfolio = [[filters.get("Portfolio")]]

    item_list = frappe.db.sql("""SELECT name, item_group, symbol FROM `tabItem` WHERE docstatus = 0""", as_dict=1)

    for portf in portfolio:
        for item in item_list:
            last_price = frappe.db.sql("""SELECT name, price, price_date FROM `tabPrice Tracker`
            WHERE docstatus=0 AND investment = '%s' %s
            ORDER BY price_date DESC LIMIT 1""" % (item.name, cond_ptrack), as_dict=1)
            transactions = 0
            qty = 0
            total_cost = 0
            total_sell = 0
            total_qty = 0
            div = 0
            dop = getdate("2199-12-31")
            dos = getdate("1900-01-01")
            tot_days = 0
            for trans in invst_tran:
                if item.name == trans.investment_name and portf[0] == trans.portfolio:
                    transactions += 1
                    if trans.get("type_of_transaction") == "Buy":
                        qty += trans.get("quantity")
                        total_cost += trans.get("total")
                        total_qty += trans.get("quantity")
                        if trans.get("date") < dop:
                            dop = trans.get("date")
                    elif trans.get("type_of_transaction") == "Sell":
                        qty -= trans.get("quantity")
                        total_sell += trans.get("total")
                        if trans.get("date") > dos:
                            dos = trans.get("date")
                    elif trans.get("type_of_transaction") == "Dividend":
                        div += trans.get("total")
            if transactions > 0:
                if dos < dop:
                    dos = getdate(nowdate())
                tot_days = (dos - dop).days
                av_price = total_cost / total_qty
                if qty > 0:
                    if total_sell == 0:
                        profit = 0
                        unrel_profit = (qty * last_price[0].price) - total_cost
                    else:
                        unrel_profit = qty * (last_price[0].price - av_price)
                        profit = total_sell - total_cost
                else:
                    profit = total_sell - total_cost
                    unrel_profit = 0
                roi = (unrel_profit + profit + div) / total_cost
                ann_roi = pow((1 + roi), (365 / tot_days)) - 1
                if zero_invest == 1:
                    row = [portf[0], item.name, item.item_group, item.symbol, qty, av_price, total_cost, profit,
                           unrel_profit, div, unrel_profit + profit + div, roi * 100, ann_roi * 100,
                           last_price[0].price_date, last_price[0].price, qty*last_price[0].price]
                    data.append(row)
                else:
                    if qty > 0:
                        row = [portf[0], item.name, item.item_group, item.symbol, qty, av_price, total_cost, profit,
                               unrel_profit, div, unrel_profit + profit + div, roi * 100, ann_roi * 100,
                               last_price[0].price_date, last_price[0].price, qty*last_price[0].price]
                        data.append(row)
    return data


def get_conditions(filters):
    cond_it = ""
    cond_itd = ""
    cond_ptrack = ""

    if filters.get("date"):
        cond_itd += " AND itd.date <= '%s'" % filters.get("date")
        cond_ptrack += " AND price_date <= '%s'" % filters.get("date")

    if filters.get("portfolio"):
        cond_itd += " AND it.portfolio = '%s'" % filters.get("portfolio")

    if filters.get("investment"):
        cond_itd += " AND itd.investment_name = '%s'" % filters.get("investment")

    return cond_it, cond_itd, cond_ptrack
