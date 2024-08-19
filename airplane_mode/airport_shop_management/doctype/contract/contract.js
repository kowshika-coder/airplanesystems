// Copyright (c) 2024, v01 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Contract", {
	refresh(frm) {

	},
    onload: function(frm) {
        frm.set_query('shop', function() {
            return {
                filters: {
                    'status': 'Available'
                }
            };
        });
    },
    payment_term: function(frm) {
        if(frm.doc.payment_term == 'Monthly'){
            frm.set_df_property('date', 'reqd', 1);

        }
        else{
            frm.set_df_property('date', 'reqd', 0);
        }
    },
});
