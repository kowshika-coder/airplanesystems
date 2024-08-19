// Copyright (c) 2024, v01 and contributors
// For license information, please see license.txt

// frappe.query_reports["Crew Members"] = {
// 	"filters": [

// 	]
// };

// Copyright (c) 2024, v01 and contributors
// For license information, please see license.txt

frappe.query_reports["Crew Members"] = {
	"filters": [
        {
            "fieldname": "airplane_flight",
            "label": __("Airplane Flight"),
            "fieldtype": "Data",
            "hidden": 1,
			"default": frappe.get_route()[2] || null
        }
    ]
};

