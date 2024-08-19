# Copyright (c) 2024, v01 and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    airport_name = filters.get("airport_name") if filters else None
    
    columns = [
        {"fieldname": "no", "label": "Shop Number", "fieldtype": "Data"},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 200},
    ]
    
    data = []
    status_counts = {}

    if airport_name:
        shops = frappe.db.get_all('Shop', filters={'airport': airport_name}, fields=['no', 'status', 'name'])
        for shop in shops:
            link = f'<a href="/app/Form/Shop/{shop.name}">{shop.no}</a>'
            data.append([link, shop.status])            
            if shop.status in status_counts:
                status_counts[shop.status] += 1
            else:
                status_counts[shop.status] = 1
    else:
        shops = frappe.db.get_all('Shop',fields=['no', 'status', 'name'])
        for shop in shops:
            link = f'<a href="/app/Form/Shop/{shop.name}">{shop.no}</a>'
            data.append([link, shop.status])            
            if shop.status in status_counts:
                status_counts[shop.status] += 1
            else:
                status_counts[shop.status] = 1
    chart_data = {
        'data': {
            'labels': list(status_counts.keys()),
            'datasets': [{'values': list(status_counts.values())}]
        },
        'type': 'bar'
    }
    
    return columns, data, None, chart_data
