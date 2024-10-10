import frappe
from datetime import date,datetime


def check_date_of_expiry():
    current_date = str(date.today())
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    get_contracts=frappe.db.get_all('Contract',filters={'docstatus':['in',[0,1]]},fields=['name','date_of_expiry','shop'])
    for contract in get_contracts:
        print(f'--------------------------------------------------------------------------------------------------------------')
        try:
            date_of_expiry=str(contract.date_of_expiry)
            expiry_date = datetime.strptime(date_of_expiry, "%Y-%m-%d")
            status_update=frappe.get_doc('Contract',contract.name)
            shop_update=frappe.get_doc('Shop',contract.shop)
            if expiry_date < current_date:
                if status_update.status == 'Current':
                    shop_update.status='Available'
                status_update.status='Expired'
            else:
                shop_update.status='Occupied'
                status_update.status='Current'
            shop_update.save(ignore_version=True)
            status_update.save(ignore_version=True)
            frappe.db.commit()
        except:
            pass
    return


def send_mail_to_tenant():
    current_date=datetime.now()
    today=current_date.date().day
    Contracts = frappe.get_all('Contract', filters={'payment_term':'Monthly','payment_status':'Pending','date':['<', today]},fields=['name','tenant'])
    for contract in Contracts:
        get_tenant=frappe.get_doc('Tenant Information',contract['tenant'])
        email_id=get_tenant.email_id
        subject = "Reminder: Rent Due Soon"
        message = f"Dear {get_tenant.first_name},<br><br>Your rent is on due. Please ensure it is paid on time to avoid any late fees.<br><br>Thank you."
        frappe.sendmail(recipients=email_id,subject=subject,message=message)
        # frappe.enqueue('send_mail_immediate', recipients=email_id, subject=subject, message=message,queue='long')


def check_for_reminder():
    tenant_notification=frappe.db.get_single_value("Airport Shop Settings","rent_reminders")
    if tenant_notification == 'Enable':
        frappe.db.set_value('Scheduled Job Type', 'contract.update_contract_payment_status', 'stopped', False)
    else:
        frappe.db.set_value('Scheduled Job Type', 'contract.update_contract_payment_status', 'stopped', True)

def send_loader():
    frappe.enqueue(check_for_reminder,queue='long')
    #frappe.
    print(10)
    print(11)