# Copyright (c) 2024, v01 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime,timedelta
import calendar


class Contract(Document):
    def validate(self):
        if not self.amount:
            self.amount = frappe.db.get_single_value("Airport Shop Settings","standard_rent_amount")
        check_opened_contracts=frappe.db.count('Contract',filters={'docstatus':1,'status':'Current','shop':self.shop})
        if check_opened_contracts != 0:
            frappe.throw('This shop has other Active Contract')
        self.payment_status = 'Pending'
    pass

    def before_submit(self):
        check_opened_contracts=frappe.db.count('Contract',filters={'docstatus':1,'status':'Current','shop':self.shop})
        if check_opened_contracts == 0:
            frappe.db.set_value('Shop', self.shop, 'status', 'Occupied')
        create_payment_receipt(self,self.shop,self.tenant,self.payment_term,self.amount,self.name,self.from_date,self.date_of_expiry)
pass


def create_payment_receipt(self,shop, tenant, payment_term, lease_amount, contract_id, started_date, date_of_expiry):
    sql_query = """
INSERT INTO `tabPayment Receipt` (shop, tenant, contract, amount_paid,name,workflow_state,month,year,payment_month)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
    current_date=datetime.now()
    pending_count=frappe.db.count('Payment Receipt',filters={'month': ['<=', current_date.month],'year': ['<=', current_date.year],'contract':contract_id,'payment_status':'Unpaid'})
    update_contract_payment_status(self,contract_id,pending_count)
    existing_count=frappe.db.count('Payment Receipt',filters={'contract':contract_id})+1
    start_date = datetime.strptime(started_date, "%Y-%m-%d")
    end_date = datetime.strptime(date_of_expiry, "%Y-%m-%d")
    name=f'PR-{contract_id}-{str(existing_count).zfill(3)}'
    if payment_term == 'Monthly':
        total_months = months_diff(started_date, date_of_expiry)
        lease_amount_per_month = lease_amount / total_months
        while start_date <= end_date:
            month_to_add = start_date.strftime("%m")
            year_to_add=start_date.strftime("%Y")
            payment_month=f'{year_to_add}-{month_to_add}-01'
            payment_month = datetime.strptime(payment_month, '%Y-%m-%d')
            values = (shop, tenant, contract_id, lease_amount_per_month,name,'Pending',month_to_add,year_to_add,payment_month)
            frappe.db.sql(sql_query, values)
            frappe.db.commit()
            existing_count+=1
            start_date += timedelta(days=31) 
            name=f'PR-{contract_id}-{str(existing_count).zfill(3)}'
    else:
        month_to_add = start_date.strftime("%m")
        year_to_add=start_date.strftime("%Y")
        payment_month=f'{year_to_add}-{month_to_add}-01'
        payment_month = datetime.strptime(payment_month, '%Y-%m-%d')
        values = (shop, tenant, contract_id, lease_amount,name,'Pending',month_to_add,year_to_add,payment_month)
        frappe.db.sql(sql_query, values)
        frappe.db.commit()

def months_diff(date1_str, date2_str):
    date_format = "%Y-%m-%d"
    date1 = datetime.strptime(date1_str, date_format)
    print(f'date1 {date1}')
    date2 = datetime.strptime(date2_str, date_format)
    print(f'date1 {date1}, date2 {date2}')
    month_diff = (date2.year - date1.year) * 12 + date2.month - date1.month +1
    return abs(month_diff)


def update_contract_payment_status(self=None,contract_id = None,pending_count = None):
    current_date=datetime.now()
    if contract_id:
        paymentvalue='Pending' if pending_count > 0 else 'Paid'
        frappe.db.set_value('Contract', contract_id, 'payment_status', paymentvalue)
    else:
        get_all_contracts=frappe.db.get_all('Contract',filters={'status':'Current'})
        for contract in get_all_contracts:
            pending_count=frappe.db.count('Payment Receipt',filters={'month': ['>=', current_date.month],'year': ['>=', current_date.year],'contract':contract['name'],'payment_status':'Unpaid'})
            paymentvalue='Pending' if pending_count > 0 else 'Paid'
            frappe.db.set_value('Contract', contract['name'], 'payment_status', paymentvalue)