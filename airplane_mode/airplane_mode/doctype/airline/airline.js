frappe.ui.form.on("Airline", {
    refresh: function(frm) {
        if (frm.doc.website) {
            frm.add_web_link(__(frm.doc.website),'View Website' );
        }
    }
});
