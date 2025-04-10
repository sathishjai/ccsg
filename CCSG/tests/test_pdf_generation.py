# tests/test_pdf_generation.py
import unittest
import os
import sys
from datetime import datetime, date, timedelta
import tempfile

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pdf_generator.pdf_builder import PDFBuilder
from pdf_generator.template_manager import TemplateManager
from models.customer import Customer
from models.account import Account
from models.transaction import Transaction
from processors.financial_calculator import FinancialCalculator
from database.connection import db

class TestPdfGeneration(unittest.TestCase):
    """Test PDF generation for credit card statements"""
    
    def setUp(self):
        """Set up test environment"""
        self.connection = db.connect()
        
        # Clear test data
        cursor = self.connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE transactions")
        cursor.execute("TRUNCATE TABLE accounts")
        cursor.execute("TRUNCATE TABLE customers")
        cursor.execute("TRUNCATE TABLE billing_cycles")
        cursor.execute("TRUNCATE TABLE interest_calculations")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        self.connection.commit()
        
        # Create test customer and account
        self.test_customer = Customer(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone="+60123456789",
            address_line1="123 Test Street",
            city="Test City",
            state="Test State",
            postal_code="12345",
            country="Malaysia",
            date_of_birth=date(1990, 1, 1)
        )
        self.test_customer.save()
        
        self.test_account = Account(
            customer_id=self.test_customer.customer_id,
            account_number="TEST0001234567",
            card_number="5196061234567890",
            card_type="MASTERCARD",
            credit_limit=10000.00,
            current_balance=1000.00,
            statement_date=15,
            payment_due_date=10,
            annual_interest_rate=18.00,
            opening_date=date.today() - timedelta(days=90)
        )
        self.test_account.save()
        
        # Create test transactions
        self.create_test_transactions()
        
        # Create a billing cycle for testing
        self.calculator = FinancialCalculator()
        today = date.today()
        statement_month = today.replace(day=1) - timedelta(days=1) if today.day < 15 else today
        self.statement_start = statement_month.replace(day=16)  # 16th of previous month
        if today.day < 15:
            self.statement_end = today.replace(day=15, month=today.month-1)  # 15th of previous month
        else:
            self.statement_end = today.replace(day=15)  # 15th of current month
        
        self.cycle_id = self.calculator.create_billing_cycle(
            self.test_account.account_id,
            self.statement_start,
            self.statement_end
        )
        
        # Calculate interest
        self.calculator.calculate_interest(self.test_account.account_id, self.cycle_id)
        
        # Update summary
        self.calculator.calculate_statement_summary(self.test_account.account_id, self.cycle_id)
        
        # Create template manager and PDF builder
        self.template_manager = TemplateManager()
        self.pdf_builder = PDFBuilder(self.template_manager)
    
    def tearDown(self):
        """Clean up after test"""
        db.close()
    
    def create_test_transactions(self):
        """Create test transactions for the statement period"""
        # Get dates for the statement period
        today = date.today()
        prev_month = today.replace(day=1) - timedelta(days=1)
        start_date = prev_month.replace(day=16)  # 16th of previous month
        end_date = today.replace(day=15)  # 15th of current month
        
        # Create some purchases
        for i in range(1, 6):
            transaction_date = start_date + timedelta(days=i * 5)
            if transaction_date <= end_date:
                transaction = Transaction(
                    account_id=self.test_account.account_id,
                    transaction_date=datetime.combine(transaction_date, datetime.min.time()),
                    posting_date=datetime.combine(transaction_date + timedelta(days=1), datetime.min.time()),
                    merchant_name=f"TEST MERCHANT {i}",
                    merchant_category="Shopping",
                    amount=-200.00,  # 200 per transaction
                    description=f"Test purchase {i}",
                    reference_number=f"REF{i}",
                    transaction_type="PURCHASE",
                    currency="MYR"
                )
                transaction.save()
                transaction.update_account_balance()
        
        # Create a payment
        payment_date = start_date + timedelta(days=20)
        if payment_date <= end_date:
            payment = Transaction(
                account_id=self.test_account.account_id,
                transaction_date=datetime.combine(payment_date, datetime.min.time()),
                posting_date=datetime.combine(payment_date, datetime.min.time()),
                merchant_name="CIMB PAYMENT",
                amount=500.00,  # 500 payment
                description="Test payment",
                reference_number="PAYREF1",
                transaction_type="PAYMENT",
                currency="MYR"
            )
            payment.save()
            payment.update_account_balance()
    
    def test_template_loading(self):
        """Test loading of the CIMB template"""
        template = self.template_manager.get_template("CIMB")
        self.assertIsNotNone(template)
        self.assertEqual(template.name, "CIMB")
    
    def test_pdf_generation(self):
        """Test generating a PDF statement"""
        # Create a temporary file for the PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            pdf_path = temp_file.name
        
        try:
            # Generate the PDF
            result = self.pdf_builder.generate_statement(
                self.test_account.account_id,
                self.cycle_id,
                output_path=pdf_path
            )
            
            # Check if the PDF was generated
            self.assertTrue(result['success'])
            self.assertTrue(os.path.exists(pdf_path))
            self.assertGreater(os.path.getsize(pdf_path), 0)
            
            # Update the billing cycle with the PDF path
            query = """
                UPDATE billing_cycles 
                SET statement_generated = 1, pdf_file_path = %s 
                WHERE cycle_id = %s
            """
            db.execute_query(query, (pdf_path, self.cycle_id))
            
            # Verify the update
            query = "SELECT * FROM billing_cycles WHERE cycle_id = %s"
            result = db.execute_query(query, (self.cycle_id,), fetch=True)
            self.assertEqual(result[0]['statement_generated'], 1)
            self.assertEqual(result[0]['pdf_file_path'], pdf_path)
            
        finally:
            # Clean up the temporary file
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
    
    def test_statement_data_preparation(self):
        """Test preparation of statement data"""
        # Get statement data
        statement_data = self.pdf_builder.prepare_statement_data(
            self.test_account.account_id,
            self.cycle_id
        )
        
        # Check basic information
        self.assertEqual(statement_data['account']['account_number'], self.test_account.account_number)
        self.assertEqual(statement_data['customer']['first_name'], self.test_customer.first_name)
        self.assertEqual(statement_data['customer']['last_name'], self.test_customer.last_name)
        
        # Check billing cycle information
        self.assertEqual(statement_data['billing_cycle']['start_date'], self.statement_start)
        self.assertEqual(statement_data['billing_cycle']['end_date'], self.statement_end)
        
        # Check transactions
        self.assertGreater(len(statement_data['transactions']), 0)
        
        # Check that transactions are within the statement period
        for transaction in statement_data['transactions']:
            transaction_date = transaction['transaction_date'].date() if isinstance(transaction['transaction_date'], datetime) else transaction['transaction_date']
            self.assertTrue(self.statement_start <= transaction_date <= self.statement_end)

if __name__ == "__main__":
    unittest.main()