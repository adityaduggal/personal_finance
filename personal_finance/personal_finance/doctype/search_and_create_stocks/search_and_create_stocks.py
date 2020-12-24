# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aditya Duggal and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import re
import frappe
from frappe.model.document import Document
from ...api.nse_tools.nse_api import get_code_list
from ...api.mf_api.mf_api import get_all_mf_codes


class SearchandCreateStocks(Document):

	def search_keyword(self):
		self.search_results = []
		if self.keyword:
			without_spaces = (self.keyword).replace(" ", "")
			if len(without_spaces) < 3:
				frappe.throw("Use atleast 3 Letters to Search")
			else:
				results = frappe._dict({})
				if self.type in ("Stock", "Index"):
					all_codes = get_code_list(self.type)
					for k in all_codes:
						if re.search(self.keyword, k, re.IGNORECASE):
							results["symbol"] = k
							results["company_name"] = all_codes.get(k)
							results["type"] = self.type
							self.append("search_results", results.copy())
						elif re.search(self.keyword, all_codes.get(k), re.IGNORECASE):
							results["symbol"] = k
							results["company_name"] = all_codes.get(k)
							results["type"] = self.type
							self.append("search_results", results.copy())
					if not results:
						frappe.msgprint("No Results Found")
				elif self.type == "Mutual Fund":
					all_codes = get_all_mf_codes()
					for k in all_codes:
						k = frappe._dict(k)
						if re.search(self.keyword, str(k.schemeCode), re.IGNORECASE):
							results["symbol"] = k.schemeCode
							results["company_name"] = k.schemeName
							results["type"] = self.type
							self.append("search_results", results.copy())
						elif re.search(self.keyword, k.schemeName, re.IGNORECASE):
							results["symbol"] = k.schemeCode
							results["company_name"] = k.schemeName
							results["type"] = self.type
							self.append("search_results", results.copy())
					if not results:
						frappe.msgprint("No Results Found")
				else:
					frappe.msgprint(f"{self.type} Selected is Not Covered Yet")
