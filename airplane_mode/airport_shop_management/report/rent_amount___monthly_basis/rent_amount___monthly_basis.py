import frappe

def execute(filters=None):
    columns = [
        {"label": "Month", "fieldname": "month", "fieldtype": "Data", "width": 100},
        {"label": "Total Amount", "fieldname": "total_amount", "fieldtype": "Currency", "width": 120}
    ]
    
    query = """
    SELECT
        DATE_FORMAT(payment_date, '%Y-%m') AS month,
        SUM(amount_paid) AS total_amount
    FROM
        `tabPayment Receipt`
    GROUP BY
        DATE_FORMAT(payment_date, '%Y-%m')
    ORDER BY
        month DESC
    """
    
    data = frappe.db.sql(query, as_dict=True)
    
    return columns, data
