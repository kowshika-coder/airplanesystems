# Copyright (c) 2024, v01 and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
import random,string


class AirplaneTicket(WebsiteGenerator):
	def before_save(self):
		airplane_flight=frappe.get_doc('Airplane Flight',self.flight).airplane
		airplane=frappe.get_doc('Airplane',airplane_flight)
		airplane_name=airplane.name
		total_flights=frappe.get_all('Airplane Flight',filters={'airplane':airplane_name})
		total_flights=[flight['name'] for flight in total_flights]
		flight_capacity=airplane.capacity
		current_capacity = frappe.db.count('Airplane Ticket', filters={'flight': ['in', total_flights]})+1
		if flight_capacity < current_capacity:
			frappe.throw("The airplane's capacity is already full.", frappe.ValidationError)
		if not self.seat:
			random_number=random.randint(1,100)
			all_letters = 'ABCDE'
			random_alpha=random.choice(all_letters)
			self.seat=f'{random_number}{random_alpha}'
		update_ticket_gate(self)
			
	def validate(self):
		seen_types = set()
		unique_add_ons = []

		for addon in self.add_ons:
			addon_type = addon.get('item') 
			print(f'-----------------addon_type {addon_type}')
			if addon_type not in seen_types:
				seen_types.add(addon_type)
				unique_add_ons.append(addon)

		self.add_ons = unique_add_ons

		total_amount = self.flight_price
		for addon in self.add_ons:
			total_amount += addon.get('amount', 0.0)

		self.total_amount = total_amount
		# #self.add_ons ------------------------- [<AirplaneTicketAddonItem: eskvn3ctms parent=Qantas Airways-005-07-2024-00013-MAA-to-DXB-021>, <AirplaneTicketAddonItem: eskvhfihaq parent=Qantas Airways-005-07-2024-00013-MAA-to-DXB-021>, <AirplaneTicketAddonItem: eskv95v0j6 parent=Qantas Airways-005-07-2024-00013-MAA-to-DXB-021>]

		# Addonamount=0
		# for i in self.add_ons:
		# 	print(f't------------- ype {i.item}')
		# 	Addonamount+=i.amount
		# Total_price=self.flight_price+Addonamount
		# print(f'Addonamount {Addonamount}')
		# self.total_amount = f'{Total_price}'

	def before_submit(self):
		update_ticket_gate(self)
		if self.status !='Boarded':
			frappe.throw("Flight is not Boarded")

	pass

def update_ticket_gate(self):
	airplane_flight=frappe.get_doc('Airplane Flight',self.flight).gate_number
	if airplane_flight:
		self.gate_number=airplane_flight
		self.gate_status="Assigned"

