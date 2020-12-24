# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import requests
import frappe


def get_all_mf_codes():
    link = get_mf_link() + "mf"
    results = requests.get(link)
    return results.json()


def get_mf_quote(scheme_code):
    link = get_mf_link() + "mf/" + str(scheme_code)
    results = requests.get(link)
    results = results.json()
    if results.get("status", "FAIL") == "SUCCESS":
        results = frappe._dict(results)
        return results
    else:
        print(f"No Results found for {scheme_code}")
        frappe.msgprint(f"No Results found for {scheme_code}")


def get_mf_link():
    return "https://api.mfapi.in/"
