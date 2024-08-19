# Copyright (c) 2024, v01 and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    airport_name = filters.get("airplane_flight") if filters else None    
    columns = [
        {"fieldname": "member_id", "label": "Member ID", "fieldtype": "Data"},
        {"fieldname": "role", "label": "Role", "fieldtype": "Data", "width": 200},
    ]
    
    data = []
    status_counts = {}
    gate_number={}

    if airport_name:
        try:
            gate_number=frappe.get_doc("Airplane Flight", airport_name).gate_number
            if gate_number:
                gate_number = f'<b>Gate Number:</b> {frappe.get_doc("Gates", gate_number).no}'
            else:
                gate_number=f'Gate Number Not Assigned'
        except:
            gate_number=f'Gate Number Not Assigned'
        members = frappe.db.get_all('Crew Member Item', filters={'parent': airport_name}, fields=['name', 'name1', 'role'])
        for member in members:
            link = f'<a href="/app/crew-member/{member.name1}">{member.name1}</a>'
            get_role=frappe.get_doc('Crew Member Role',member.role)
            data.append([link, get_role.role])            
            if get_role.role in status_counts:
                status_counts[get_role.role] += 1
            else:
                status_counts[get_role.role] = 1
    else:
        frappe.throw('Select Airplane Flight')
    chart_data = {
        'data': {
            'labels': list(status_counts.keys()),
            'datasets': [{'values': list(status_counts.values())}]
        },
        'type': 'pie'
    }
    
    return columns, data, gate_number,chart_data
