// Copyright (c) 2024, v01 and contributors
// For license information, please see license.txt


// Custom Script for a specific page or doctype




    frappe.ui.form.on('Payment Receipt', {
        refresh: function(frm) {
            if(frm.doc.payment_status == "Paid"){
            frm.add_custom_button(__('Send Payment Receipt To Tenant'), function() {
                frappe.call({
                    method: 'airplane_mode.airport_shop_management.doctype.payment_receipt.payment_receipt.send_mail_to_tenant',
                    args: {
                        self_name: frm.doc.name 
                    },
                    callback: function(response) {
                        frappe.msgprint(response.message);
                    },
                    error: function(err) {
                        frappe.msgprint(__('An error occurred: ') + err.message);
                    }
                });
            })
        }
        }
    }) 
    //         if (frappe.user_roles.includes("Tenant")) {
    //             const current_date = frappe.datetime.nowdate();
    //             const first_day_current_month = frappe.datetime.get_first_day(current_date);
    //             const first_day_previous_month = frappe.datetime.add_months(first_day_current_month, -1);
    //             alert(first_day_current_month)
    //             frm.set_query("payment_date", function() {
    //                 return {
    //                     filters: [
    //                         ["payment_date", ">=", first_day_previous_month],
    //                         ["payment_date", "<=", current_date]
    //                     ]
    //                 };
    //             });
    //         }
    //     }
    // });


    // frappe.listview_settings['Payment Receipt'] = {
    //     onload: function(listview) {
    //         alert(3)
    //         // Check if the user has the Tenant role
    //         if (frappe.user_roles.includes("Tenant")) {
    //             const current_date = frappe.datetime.nowdate();
    //             const first_day_current_month = frappe.datetime.get_first_day(current_date);
    //             const first_day_previous_month = frappe.datetime.add_months(first_day_current_month, -1);
    
    //             // Apply filters to the list view
    //             listview.filter_area.add([
    //                 ["Payment Receipt", "payment_date", ">=", first_day_previous_month],
    //                 ["Payment Receipt", "payment_date", "<=", current_date]
    //             ]);
    //         }
    //     }
    // };
    
