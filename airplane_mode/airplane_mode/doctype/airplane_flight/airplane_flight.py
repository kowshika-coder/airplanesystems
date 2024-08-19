# Copyright (c) 2024, v01 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def before_submit(self):
		self.status="Completed"
		update_gate_num(self)
		return
	def before_save(self):
		self.departure_details=f'{self.date_of_departure} {self.time_of_departure}'
		update_gate_num(self)	
	def on_update_after_submit(self):
		update_gate_num(self)	
	
	pass



def update_gate_num(self):
	if self.gate_number:
		records = frappe.get_list('Airplane Ticket', filters={'flight': self.name}, fields=['name'])
		for rec in records:
			update_gate=frappe.get_doc('Airplane Ticket',rec['name'])
			update_gate.gate_number=self.gate_number
			update_gate.gate_status="Assigned"
			update_gate.save()
			frappe.db.commit()
			frappe.msgprint("Operation was successful!", alert=True)