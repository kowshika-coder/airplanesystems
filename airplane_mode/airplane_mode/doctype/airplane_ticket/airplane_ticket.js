// Copyright (c) 2024, v01 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
        frm.add_custom_button(__('Assign Seat'), function() {
            var default_seat_number = frm.doc.seat
            frappe.prompt({
                fieldname: 'seat_number',
                label: 'Seat Number',
                fieldtype: 'Data',
                'default':default_seat_number,
                reqd: 1
            }, function(val){   
                const regex = /^\d{2}[A-E]$/;  
                var test_data= regex.test(val.seat_number);     
                if (test_data){
                    frm.set_value('seat', val.seat_number);
                }
            }, 'Select Seat');
        })
        
	},
    update_total_amount(frm){
        let total_d=0
        for(let item of frm.doc.add_ons){
			total_d+=item.amount
		}
		const amount= total_d + frm.doc.flight_price
		frm.set_value('total_amount',amount)
    },
    flight_price(frm){
        frm.trigger('update_total_amount')
    }
});
frappe.ui.form.on("Airplane Ticket Add-on Item", {
	amount(frm) {
        frm.trigger('update_total_amount')
	},
    flight_price(frm){
        frm.trigger('update_total_amount')
    }
});
