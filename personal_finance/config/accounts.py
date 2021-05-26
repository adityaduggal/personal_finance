from frappe import _

def get_data():
    return [
        {
            "label": _("General Ledger"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Income Expense Entry",
                },
                {
                    "type": "doctype",
                    "name": "Investment Transaction",
                },
            ]
        },
        {
            "label": _("Accounting Masters"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Portfolio",
                },
            ]
        }
    ]