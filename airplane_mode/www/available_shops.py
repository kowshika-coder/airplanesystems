import frappe

def get_context(context):
    context.shops = frappe.call("airplane_mode.api.get_available_shops")
    return context
