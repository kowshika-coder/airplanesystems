# Copyright (c) 2024, v01 and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
	def before_save(self):
		last_name=''
		if self.last_name:
			last_name=f' {self.last_name}'
		self.full_name=f'{self.first_name}{last_name}'
	
