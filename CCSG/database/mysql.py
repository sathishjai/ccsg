from pymysql import connect
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
#import mysql.connector

# Sample DataFrame (replace with your own data)
data = {
    'Date': ['2025-04-01', '2025-04-05', '2025-04-10'],
    'Description': ['Grocery Store', 'Fuel Station', 'Refund - Grocery'],
    'Amount': [50.75, 30.00, -5.25],
    'Transaction Type': ['Debit', 'Debit', 'Credit']
}


'''
def get_db_connection():
    conn =connect(
        host="localhost",
        user="root",
        password="2001",
        database="cimb_credit_card"
    )
    return conn
'''
# Connecting MySQL Databases to Python and Cursor:
db = connect(host = "localhost", user = "root", password = "2001")
curs = db.cursor()
query = 'show databases'
curs.execute(query)
db=curs.fetchall()
for i in db:
    print(i)

connectivity = connect(host = "localhost", user = "root", password = "2001", database = 'cimb_credit_card')
curs = connectivity.cursor()
query = 'show tables'
curs.execute(query)
data = curs.fetchall()
for x in data:
    print(x)


query = 'select * from accounts,audit_logs,billing_cycles,customers,interest_calculations,users'
print('No.of Rows in Table :',curs.execute(query))

from fpdf import FPDF
import pandas as pd
df=pd.read_sql(query,connectivity)
print(df)

# Create a PDF object
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Set title
pdf.set_font('Arial', 'B', 16)
pdf.cell(200, 10, txt="DataFrame to PDF", ln=True, align='C')

# Set column headers
pdf.set_font('Arial', 'B', 12)
for col in df.columns:
    pdf.cell(40, 10, col, border=1, align='C')
pdf.ln()

# Add data to the PDF
pdf.set_font('Arial', '', 12)
for i in range(len(df)):
    for col in df.columns:
        pdf.cell(40, 10, str(df[col][i]), border=1, align='C')
    pdf.ln()

# Output the PDF to a file
pdf.output("dataframe_output.pdf")

print("PDF generated successfully!")



# Sample DataFrame (replace with your own data)
'''
# Function to generate PDF from DataFrame
def generate_pdf_from_dataframe(df, pdf_filename="credit_card_statement.pdf"):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter  # Define page si

    # Save the PDF
    c.save()

# Generate PDF from DataFrame
generate_pdf_from_dataframe(df)
'''