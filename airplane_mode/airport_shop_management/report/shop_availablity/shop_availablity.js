// Copyright (c) 2024, v01 and contributors
// For license information, please see license.txt

frappe.query_reports["Shop Availablity"] = {
	onload: function(report) {
        let custom_filters = {
            "fieldname": "name"
        };
        frappe.set_route("query-report", "Shop Availablity", custom_filters);
    }
};

