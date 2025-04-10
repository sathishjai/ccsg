import pymysql
from pymysql import Error
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF
#from fpdf.enums import XPos, YPos
from datetime import datetime


def generate_pdf(customer, account, transactions, rewards=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)

    # Header
    pdf.cell(w=200, h=10, text="Public Bank Credit Card Statement", align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    # Customer Info
    pdf.cell(w=200, h=10, text=f"Customer: {customer['FirstName']} {customer['LastName']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(w=200, h=10, text=f"Card Number: {account['CardNumber']} ({account['CardType']})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(w=200, h=10, text=f"Balance: RM {account['CurrentBalance']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(10)
    pdf.set_font("helvetica", size=11, style='B')
    pdf.cell(50, 10, "Date", border=1)
    pdf.cell(80, 10, "Merchant", border=1)
    pdf.cell(30, 10, "Amount", border=1)
    pdf.cell(30, 10, "Type", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("helvetica", size=10)
    for txn in transactions:
        pdf.cell(50, 10, str(txn['TransactionDate']), border=1)
        pdf.cell(80, 10, txn['MerchantName'], border=1)
        pdf.cell(30, 10, f"RM {txn['Amount']:.2f}", border=1)
        pdf.cell(30, 10, txn['TransactionType'], border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(10)

    if rewards:
        pdf.set_font("helvetica", size=12, style='B')
        pdf.cell(w=200, h=10, text="Reward Points Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("helvetica", size=10)
        pdf.cell(w=200, h=10, text=f"Available Points: {rewards['AvailablePoints']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(w=200, h=10, text=f"Total Earned: {rewards['TotalPointsEarned']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(w=200, h=10, text=f"Total Redeemed: {rewards['TotalPointsRedeemed']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Unique file name
    filename = f"statement_{account['CardNumber'].replace(' ', '')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf.output(filename)

    return os.path.abspath(filename)

class PublicBankCreditCardDB:
    def __init__(self, host, user, password, database=None):
        """Initialize database connection"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Connect to MySQL server"""
        try:
            if self.database:
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    cursorclass=pymysql.cursors.DictCursor
                )
            else:
                # Connect without specifying database (for initial setup)
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    cursorclass=pymysql.cursors.DictCursor
                )
            
            self.cursor = self.connection.cursor()
            return True
        except Error as e:
            print(f"Error connecting to MySQL server: {e}")
            return False
    
    def create_database(self):
        """Create database if it doesn't exist"""
        try:
            if not self.connection:
                self.connect()
            return True
        except Error as e:
            print(f"Error creating database: {e}")
            return False
    
    def setup_database(self, sql_file_path):
        """Execute SQL from file to set up database schema and sample data"""
        try:
            if not self.connection:
                self.connect()
            
            # Switch to the database
            self.cursor.execute("USE public_bank_credit_card")
            
            # Read SQL file
            with open(sql_file_path, 'r') as file:
                sql_script = file.read()
            
            # Split script into individual statements and execute
            statements = sql_script.split(';')
            for statement in statements:
                if statement.strip():
                    self.cursor.execute(statement)
            
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error setting up database: {e}")
            return False
    
    def get_customer_info(self, customer_id):
        """Get customer information by ID"""
        try:
            query = "SELECT * FROM Customers WHERE CustomerID = %s"
            self.cursor.execute(query, (customer_id,))
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error retrieving customer info: {e}")
            return None
    
    def get_customer_accounts(self, customer_id):
        """Get all credit card accounts for a customer"""
        try:
            query = "SELECT * FROM CreditCardAccounts WHERE CustomerID = %s"
            self.cursor.execute(query, (customer_id,))
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Error retrieving customer accounts: {e}")
            return None
    
    def get_account_transactions(self, account_id, start_date=None, end_date=None):
        """Get transactions for an account with optional date filtering"""
        try:
            if start_date and end_date:
                query = """
                SELECT t.*, c.CategoryName 
                FROM Transactions t
                LEFT JOIN TransactionCategories c ON t.CategoryID = c.CategoryID
                WHERE t.AccountID = %s AND t.TransactionDate BETWEEN %s AND %s
                ORDER BY t.TransactionDate DESC
                """
                self.cursor.execute(query, (account_id, start_date, end_date))
            else:
                query = """
                SELECT t.*, c.CategoryName 
                FROM Transactions t
                LEFT JOIN TransactionCategories c ON t.CategoryID = c.CategoryID
                WHERE t.AccountID = %s
                ORDER BY t.TransactionDate DESC
                """
                self.cursor.execute(query, (account_id,))
            
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Error retrieving account transactions: {e}")
            return None
    
    def get_reward_points(self, account_id):
        """Get reward points for an account"""
        try:
            query = """
            SELECT SUM(PointsEarned) - SUM(PointsRedeemed) AS AvailablePoints,
                   SUM(PointsEarned) AS TotalPointsEarned,
                   SUM(PointsRedeemed) AS TotalPointsRedeemed
            FROM RewardPoints
            WHERE AccountID = %s AND Status = 'Active'
            """
            self.cursor.execute(query, (account_id,))
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Error retrieving reward points: {e}")
            return None
    
    def add_transaction(self, account_id, merchant_name, amount, transaction_type, 
                        category_id, description=None, merchant_location=None,
                        merchant_category=None, reference=None):
        """Add a new transaction"""
        try:
            # First get the current balance
            self.cursor.execute("SELECT CurrentBalance, AvailableCredit, CreditLimit FROM CreditCardAccounts WHERE AccountID = %s", 
                              (account_id,))
            account = self.cursor.fetchone()
            
            if not account:
                print(f"Account {account_id} not found")
                return False
            
            current_balance = account['CurrentBalance']
            available_credit = account['AvailableCredit']
            credit_limit = account['CreditLimit']
            
            # Calculate new balance based on transaction type
            new_balance = current_balance
            new_available_credit = available_credit
            
            if transaction_type == 'Purchase' or transaction_type == 'Fee' or transaction_type == 'Cash Advance':
                new_balance += amount
                new_available_credit -= amount
            elif transaction_type == 'Payment' or transaction_type == 'Refund':
                new_balance -= amount
                new_available_credit += amount
            
            # Check if transaction would exceed credit limit
            if transaction_type == 'Purchase' and new_balance > credit_limit:
                print(f"Transaction would exceed credit limit of {credit_limit}")
                return False
            
            # Insert transaction
            transaction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = """
            INSERT INTO Transactions (AccountID, TransactionDate, PostedDate, MerchantName, 
                                     MerchantLocation, MerchantCategory, Amount, TransactionType, 
                                     CategoryID, Description, Reference)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (
                account_id, transaction_date, transaction_date, merchant_name, 
                merchant_location, merchant_category, amount, transaction_type, 
                category_id, description, reference
            ))
            
            # Get the last insert ID
            transaction_id = self.connection.insert_id()
            
            # Update account balance
            update_query = """
            UPDATE CreditCardAccounts 
            SET CurrentBalance = %s, AvailableCredit = %s
            WHERE AccountID = %s
            """
            self.cursor.execute(update_query, (new_balance, new_available_credit, account_id))
            
            # Add reward points if applicable (for purchases)
            if transaction_type == 'Purchase':
                # Simple points calculation: 1 point per 10 currency spent
                points = int(amount / 10)
                if points > 0:
                    point_query = """
                    INSERT INTO RewardPoints (AccountID, TransactionID, PointsEarned, Description, ExpiryDate)
                    VALUES (%s, %s, %s, %s, DATE_ADD(CURRENT_DATE(), INTERVAL 2 YEAR))
                    """
                    self.cursor.execute(point_query, (
                        account_id, transaction_id, points, f"Points for {merchant_name} purchase"
                    ))
            
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error adding transaction: {e}")
            self.connection.rollback()
            return False
    
    def generate_statement(self, account_id):
        """Generate a statement for an account"""
        try:
            # Get account information
            self.cursor.execute("SELECT * FROM CreditCardAccounts WHERE AccountID = %s", (account_id,))
            account = self.cursor.fetchone()
            
            if not account:
                print(f"Account {account_id} not found")
                return False
            
            # Get statement date and payment due date
            statement_date = datetime.now()
            payment_due_date = datetime.now()
            payment_due_date = payment_due_date.replace(day=payment_due_date.day + account['PaymentDueDate'])
            
            # Get previous statement balance (or 0 if first statement)
            self.cursor.execute(
                "SELECT NewBalance FROM Statements WHERE AccountID = %s ORDER BY StatementDate DESC LIMIT 1", 
                (account_id,)
            )
            prev_statement = self.cursor.fetchone()
            previous_balance = prev_statement['NewBalance'] if prev_statement else 0
            
            # Calculate totals
            self.cursor.execute(
                """
                SELECT 
                    COALESCE(SUM(CASE WHEN TransactionType = 'Purchase' OR TransactionType = 'Fee' OR TransactionType = 'Cash Advance' THEN Amount ELSE 0 END), 0) as TotalPurchases,
                    COALESCE(SUM(CASE WHEN TransactionType = 'Payment' OR TransactionType = 'Refund' THEN Amount ELSE 0 END), 0) as TotalPayments,
                    COALESCE(SUM(CASE WHEN TransactionType = 'Fee' THEN Amount ELSE 0 END), 0) as TotalFees
                FROM Transactions 
                WHERE AccountID = %s AND StatementID IS NULL
                """, 
                (account_id,)
            )
            totals = self.cursor.fetchone()
            
            # Calculate interest (simplified - in reality would be more complex)
            # Using simple interest calculation for demonstration
            interest = previous_balance * (account['InterestRate'] / 100 / 12)
            
            # Calculate new balance
            new_balance = previous_balance + totals['TotalPurchases'] - totals['TotalPayments'] + interest
            
            # Calculate minimum payment
            minimum_payment = max(new_balance * (account['MinimumPaymentPercentage'] / 100), 50)  # Min 50 currency units
            
            # Create statement
            query = """
            INSERT INTO Statements (AccountID, StatementDate, PaymentDueDate, PreviousBalance, 
                                   NewBalance, MinimumPayment, TotalPurchases, TotalPayments, 
                                   TotalFees, TotalInterest, Status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Generated')
            """
            self.cursor.execute(query, (
                account_id, statement_date, payment_due_date, previous_balance, 
                new_balance, minimum_payment, totals['TotalPurchases'], 
                totals['TotalPayments'], totals['TotalFees'], interest
            ))
            
            # Get statement ID
            statement_id = self.connection.insert_id()
            
            # Update transactions to link them to this statement
            self.cursor.execute(
                "UPDATE Transactions SET StatementID = %s WHERE AccountID = %s AND StatementID IS NULL", 
                (statement_id, account_id)
            )
            
            self.connection.commit()
            return statement_id
        except Error as e:
            print(f"Error generating statement: {e}")
            self.connection.rollback()
            return False
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            if self.cursor:
                self.cursor.close()
            self.connection.close()


# Example usage
if __name__ == "__main__":
    # Replace with your MySQL server credentials
    db = PublicBankCreditCardDB(
        host="localhost",
        user="root",
        password="2001"
    )
    
    # Connect to server and create database if not exists
    if db.connect():
        db.create_database()
        
        # Reconnect with database specified
        db.close_connection()
        db = PublicBankCreditCardDB(
            host="localhost",
            user="root",
            password="2001",
            database="cimb_credit_card"
        )
        
        if db.connect():
            # To setup database using the SQL script:
            # 1. Save the MySQL script to a file
            # 2. Use the setup_database method:
            # db.setup_database('public_bank_credit_card_schema.sql')
            
            # Example: Get customer info
            customer = db.get_customer_info(1000)
            if customer:
                print(f"Customer: {customer['FirstName']} {customer['LastName']}")
            
            # Example: Get customer accounts
            accounts = db.get_customer_accounts(1000)
            if customer and accounts:
                for account in accounts:
                    transactions = db.get_account_transactions(account['AccountID'])
                    rewards = db.get_reward_points(account['AccountID'])
                    pdf_path = generate_pdf(customer, account, transactions, rewards)
                    print(f"PDF generated for {account['CardNumber']}: {pdf_path}")
            
            # Close the connection
            db.close_connection()
