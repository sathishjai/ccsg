from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(statement_data, file_name):
    c = canvas.Canvas(file_name, pagesize=letter)
    c.drawString(100, 750, f"Customer Name: {statement_data['customer_name']}")
    c.drawString(100, 735, f"Account Number: {statement_data['account_number']}")
    c.drawString(100, 720, f"Balance: {statement_data['balance']}")
    # Additional sections for transactions, summary, etc.
    c.save()
    print(c)

