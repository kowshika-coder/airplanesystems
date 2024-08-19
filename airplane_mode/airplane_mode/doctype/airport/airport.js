// Copyright (c) 2024, v01 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airport", {
	refresh(frm) {
        frm.fields_dict.view_shops.$input.addClass('btn-primary'); // Optional: Add a class to style the button
        airport_name=frm.doc.name
        frm.fields_dict.view_shops.$input.on('click', function() {
            // Navigate to a specific URL
            window.open('/app/query-report/Shop status?airport_name='+airport_name+'', '_blank');
        })

	},
});
