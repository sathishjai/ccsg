from pymysql import connect

import pymysql

# Database Connection
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="2001",
        database="cimb_credit_card",
        cursorclass=pymysql.cursors.DictCursor  # Enables dictionary-style cursor
    )

# Fetch customer details
def get_customer_data(customer_id):
    db = connect_db()
    cursor = db.cursor()

    query = "SELECT * FROM customers WHERE customer_id = %s"
    cursor.execute(query, (customer_id,))
    customer = cursor.fetchone()  # Fetch one record

    db.close()
    return customer

def get_transactions(card_id):
    db = connect_db()
    cursor = db.cursor()

    query = """SELECT transaction_date, description, amount, transaction_type 
               FROM transactions WHERE card_id = %s ORDER BY transaction_date"""
    cursor.execute(query, (card_id,))
    transactions = cursor.fetchall()  # Fetch all records

    db.close()
    return transactions

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(customer, transactions):
    filename = f"{customer['name']}_Statement.pdf"
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica", 14)
    c.drawString(100, 750, f"Credit Card Statement - {customer['name']}")

    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Customer ID: {customer['customer_id']}")
    c.drawString(100, 710, f"Email: {customer['email']}")

    y_position = 690
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "Transactions:")

    y_position -= 20
    for tx in transactions:
        c.setFont("Helvetica", 10)
        c.drawString(100, y_position, f"{tx['transaction_date']} - {tx['description']} - ${tx['amount']} ({tx['transaction_type']})")
        y_position -= 20

    c.save()
    print(f"Statement saved as {filename}")

if __name__ == "__main__":
    customer_id = 1  # Change this as needed
    customer = get_customer_data(customer_id)

    if customer:
        customer_id = 1  # Assume customer has card with ID 1
        transactions = get_transactions(customer_id)
        generate_pdf(customer, transactions)
    else:
        print("Customer not found.")
