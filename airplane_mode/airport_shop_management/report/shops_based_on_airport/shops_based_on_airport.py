# Copyright (c) 2024, v01 and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns= [{
		"fieldname":'name',
		'label':'Airport',
		'fieldtype':'Link',
		'options':'Airport'
	},
	{
		"fieldname":"shop_count",
		'label':'Total Shops',
		'fieldtype':'Data',

	}]
	airports=frappe.db.get_all('Airport',fields=['name'])
	for a_p in airports:
		a_p['shop_count']=frappe.db.count('Shop',filters={'airport':a_p['name']})
	print(f'airport ---- {airports}')
	sorted_airports = sorted(airports, key=lambda x: x['shop_count'],reverse=True)
	data = sorted_airports
	chart={
		'data':{
			'labels':[i.name for i in data],
			'datasets':[{'values':[i.shop_count for i in data]}]

		},
		'type':'pie',
	}
	return columns, data,None,chart
