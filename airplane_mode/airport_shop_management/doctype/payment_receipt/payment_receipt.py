# Copyright (c) 2024, v01 and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime,timedelta
from airplane_mode.airport_shop_management.doctype.contract.contract import update_contract_payment_status

class PaymentReceipt(Document):
	def before_save(self):
		if self.workflow_state == 'Approved':
			self.payment_status='Paid'
		get_pr=frappe.get_doc('Payment Receipt',self.name)
		if get_pr.workflow_state == 'Pending':
			self.payment_date=datetime.now()

	def validate(self):
		current_receipt=frappe.get_doc('Payment Receipt',self.name)
		if self.payment_status == 'Paid':
			frappe.throw(f'Payment Already done, No changes will be accepted {current_receipt}')

	def on_update(self):
		current_date=datetime.now()
		# today=current_date.date().day
		# Contracts = frappe.get_all('Contract', filters={'payment_term':'Monthly','payment_status':'Pending','date':['<', today]},fields=['name','tenant'])
		# for contract in Contracts:
		# 	get_tenant=frappe.get_doc('Tenant Information',contract['tenant'])
		# 	email_id=get_tenant.email_id
		# 	subject = "Reminder: Rent Due Soon"
		# 	message = f"Dear {get_tenant.first_name},<br><br>Your rent is due on {get_tenant.last_name}. Please ensure it is paid on time to avoid any late fees.<br><br>Thank you."
		# 	frappe.sendmail(recipients=email_id,subject=subject,message=message)
		pending_count=frappe.db.count('Payment Receipt',filters={'month': ['<=', current_date.month],'year': ['<=', current_date.year],'contract':self.contract,'payment_status':'Unpaid'})
		update_contract_payment_status(self,self.contract,pending_count)







@frappe.whitelist()
def send_mail_to_tenant(self_name):
	get_receipt=frappe.get_doc('Payment Receipt', self_name)
	pdf_file = frappe.attach_print('Payment Receipt', self_name, print_format='Payment Receipt Template')
	tenant = frappe.get_doc('Tenant Information', get_receipt.tenant)
	frappe.sendmail(
		recipients=tenant.email_id,
		subject=f"Rent Receipt for {get_receipt.shop}",
		message=f"Dear {tenant.first_name},<br><br>Please find attached the rent receipt for your shop {get_receipt.shop}.<br><br>Thank you.",
		attachments=[{
	'fname': 'Rent Receipt.pdf',
	'fcontent': pdf_file['fcontent'],
	}])

@frappe.whitelist()
def get_filtered_payments():
    user_roles = frappe.get_roles()
    if "Is_Tenant" in user_roles:
        current_date = frappe.utils.nowdate()
        return frappe.get_all('Payment Receipt',fields=['name', 'payment_month'],filters=[['payment_month', '<=', current_date]],limit_page_length=1000) 
    else:
        frappe.throw(_('You do not have permission to access this data.'))





