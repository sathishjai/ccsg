CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FullName VARCHAR(255),
    Address VARCHAR(255),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(20)
);

CREATE TABLE Accounts (
    AccountID INT PRIMARY KEY,
    CustomerID INT FOREIGN KEY REFERENCES Customers(CustomerID),
    CardNumber VARCHAR(16),
    AccountBalance DECIMAL(18, 2),
    MinimumPayment DECIMAL(18, 2),
    DueDate DATE
);

CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    AccountID INT FOREIGN KEY REFERENCES Accounts(AccountID),
    TransactionDate DATE,
    Amount DECIMAL(18, 2),
    Description VARCHAR(255),
    TransactionType VARCHAR(50)
);










import pyodbc

def connect_to_db():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=server_name;'
                          'DATABASE=database_name;'
                          'UID=username;'
                          'PWD=password')
    return conn












from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(statement_data, file_name):
    c = canvas.Canvas(file_name, pagesize=letter)
    c.drawString(100, 750, f"Customer Name: {statement_data['customer_name']}")
    c.drawString(100, 735, f"Account Number: {statement_data['account_number']}")
    c.drawString(100, 720, f"Balance: {statement_data['balance']}")
    # Additional sections for transactions, summary, etc.
    c.save()



