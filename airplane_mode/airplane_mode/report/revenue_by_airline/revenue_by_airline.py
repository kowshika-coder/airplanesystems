# Copyright (c) 2024, v01 and contributors
# For license information, please see license.txt

import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


def execute(filters=None):
	columns= [{
		"fieldname":'name',
		'label':'Airline',
		'fieldtype':'Link',
		'options':'Airline'
	},
	{
		"fieldname":"total_amount",
		'label':'Revenue',
		'fieldtype':'Currency',
		'options':'AED'

	}]
	flights=frappe.get_all("Airplane Ticket", fields=["flight.airplane","total_amount"])
	total_revenue = frappe.db.sql("""
        SELECT SUM(total_amount)
        FROM `tabAirplane Ticket`
    """, as_dict=True)[0]['SUM(total_amount)']
	print(f'total_revenue {total_revenue}----------------------------')
	airline=frappe.get_all("Airline", fields=["name"])
	for i in flights:
		asb=frappe.get_all("Airplane",filters={'name':i['airplane']},fields=["airline"]) or [{'airline':None}]
		for airl in airline:
			try:
				airl['total_amount']
			except:
				airl['total_amount']=0
			if airl['name'] == asb[0]['airline']:
				if airl['total_amount'] != 0:
					airl['total_amount']+=i['total_amount']
				else:
					airl['total_amount']=i['total_amount']	
	sorted_airlines = sorted(airline, key=lambda x: x['total_amount'],reverse=True)
	print(f'sorted_airlines {sorted_airlines}-----------------------')
	data=sorted_airlines
	chart={
		'data':{
			'labels':[i.name for i in data],
			'datasets':[{'values':[i.total_amount for i in data]}]

		},
		'type':'donut',
	}
	report_summary = [
    {"label":"Total Revenue","value":total_revenue,'indicator':'Green'},
	]
	return columns, data,None,chart,report_summary