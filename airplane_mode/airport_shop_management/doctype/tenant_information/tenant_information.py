# Copyright (c) 2024, v01 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TenantInformation(Document):
    def validate(self):
        get_tenant = frappe.get_value('User', {'email': self.email_id}, 'name')
        if get_tenant:
            tenant_infor = frappe.get_doc('User', get_tenant)
            tenant_infor.first_name = self.first_name
            tenant_infor.email = self.email_id
            tenant_infor.save()
            frappe.msgprint(f"User {self.email_id} updated.")
        else:
            create_user_with_role(self.email_id, self.first_name, 'is_tenant')


def create_user_with_role(email_id, first_name, role_name):
    try:
        new_user = frappe.get_doc({
            'doctype': 'User',
            'email': email_id,
            'first_name': first_name,
            'enabled': 1,
            'roles': [{'role': role_name}]
        })
        new_user.insert()
        frappe.db.commit()    
    except frappe.DuplicateEntryError:
        frappe.throw(f"User {email_id} already exists.")
    except Exception as e:
        frappe.throw(f"An error occurred: {str(e)}")



