from frappe import _

def get_data():
    return [
        {
            "label": _("Settings"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Personal Finance Settings",
                },
            ]
        }
    ]