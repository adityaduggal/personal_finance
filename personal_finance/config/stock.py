from frappe import _

def get_data():
    return [
        {
            "label": _("Items and Pricing"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Search and Create Stocks",
                },
                {
                    "type": "doctype",
                    "name": "Price Tracker",
                },
                {
                    "type": "doctype",
                    "name": "Search and Create Stocks",
                },
                {
                    "type": "doctype",
                    "name": "Price Tracker",
                }
            ]
        },
        {
            "label": _("Key Reports"),
            "items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Portfolio Status",
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Portfolio Transactions",
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Price Analysis",
                }
            ]
        },
    ]