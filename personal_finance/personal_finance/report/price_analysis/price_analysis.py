# Copyright (c) 2013, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import pandas as pd
from frappe.utils import flt
import plotly.express as px


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	sma1 = "SMA_" + str(filters.get("sma1"))
	sma2 = "SMA_" + str(filters.get("sma2"))
	ema1 = "SMA_" + str(filters.get("ema"))
	return ["Investment:Link/Item:300", "Date:Date:90", "Price:Currency:100", f"{sma1}:Currency:100",
			f"{sma2}:Currency:100", f"{ema1}:Currency:100"]


def get_data(filters):
	it_name = filters.get("investment")
	get_data2(filters, item_name=it_name)
	return []


def get_data2(filters, item_name=None):
	data = []
	sma1 = flt(filters.get("sma1"))
	sma2 = flt(filters.get("sma2"))
	ema1 = flt(filters.get("ema1"))
	if not item_name:
		item_name = 'Canara Robeco Equity Tax Saver Regular Growth'
	price_data = frappe.get_all("Price Tracker",
								filters=[["docstatus", "=", 0], ["investment", "=", item_name]],
								fields=["price_date", "price"])
	price_data = sorted(price_data, key=lambda k: k["price_date"], reverse=False)
	df = pd.DataFrame.from_records(price_data)
	df['SMA_' + str(sma1)] = df.iloc[:, 1].rolling(window=int(sma1)).mean()  # Add SMA with SMA1 period
	df['SMA_' + str(sma2)] = df.iloc[:, 1].rolling(window=int(sma2)).mean()  # Add SMA with SMA2 period
	df['EMA_' + str(ema1)] = df.iloc[:, 1].ewm(span=int(ema1), adjust=False).mean()  # Add EMA with EMA1 period

	for i in range(0, len(df)):
		row_data = [item_name, df.iloc[i]['price_date'], df.iloc[i]['price'], df.iloc[i]['SMA_' + str(sma1)],
					df.iloc[i]['SMA_' + str(sma2)], df.iloc[i]['EMA_' + str(ema1)]]
		data.append(row_data)

	trace = px.line(df, x='price_date', y=['price', 'SMA_' + str(sma1), 'SMA_' + str(sma2), 'EMA_' + str(ema1)],
					title='Price Chart for ' + item_name)
	trace.show()