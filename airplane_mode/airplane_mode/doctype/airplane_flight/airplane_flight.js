// Copyright (c) 2024, v01 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Flight", {
    refresh(frm){
        frm.add_custom_button(__('Check For Crew Members'), function() {
            frappe.set_route('app','query-report', 'Crew Members', { 'airplane_flight': frm.doc.name});
        })

    },
	onload(frm) {
        var departure_details=frm.doc.departure_details
        const combinedDateObj = new Date(departure_details);
        const now = new Date();
        const twelveHoursBefore = new Date(combinedDateObj.getTime() - (24 * 60 * 60 * 1000));
        if (now >= twelveHoursBefore) {
            frm.fields_dict['crew_members_section'].df.hidden = false;
            frm.fields_dict['table_bszx'].df.hidden = false; 
            frm.fields_dict['table_bszx'].df.reqd = true;
            frm.fields_dict['gate_number'].df.hidden = false; 
            frm.fields_dict['gate_number'].df.reqd = true;
            frm.refresh_fields();
        }
        else{
            frm.fields_dict['crew_members_section'].df.hidden = true;
            frm.fields_dict['table_bszx'].df.hidden = true;
            frm.fields_dict['table_bszx'].df.reqd = false;
            frm.fields_dict['gate_number'].df.hidden = true;
            frm.fields_dict['gate_number'].df.reqd = false;
            frm.refresh_fields();
        }
       
	},
});
