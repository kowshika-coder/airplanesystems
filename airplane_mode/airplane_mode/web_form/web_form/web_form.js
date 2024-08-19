frappe.ready(function() {
	// bind events here
	frappe.ui.form.on('Airplane Ticket', {
        onload: function(frm) {
            var flightPrice = 1000;

            frm.set_value('flight_price', flightPrice);
        }
    });
})