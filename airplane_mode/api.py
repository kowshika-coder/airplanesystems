import frappe

@frappe.whitelist(allow_guest=True)
def get_available_shops():
    shops = frappe.get_all("Shop", filters={"status": "Available"}, fields=["name","shop_name", "airport","square_feet",'no'])
    return shops
