// Copyright (c) 2024, v01 and contributors
// For license information, please see license.txt

frappe.query_reports["Shop status"] = {
	"filters": [
        {
            "fieldname": "airport_name",
            "label": __("Airport"),
            "fieldtype": "Data",
			"default": frappe.get_route()[2] || null
        }
    ]
};
