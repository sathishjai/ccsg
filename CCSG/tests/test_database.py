# tests/test_database.py
import unittest
import os
import sys
from datetime import datetime, date

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import db
from models.customer import Customer
from models.account import Account
from models.transaction import Transaction

class TestDatabaseConnection(unittest.TestCase):
    """Test the database connection and basic operations"""
    
    def setUp(self):
        """Set up test environment"""
        self.connection = db.connect()
        
        # Clear test data
        cursor = self.connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE transactions")
        cursor.execute("TRUNCATE TABLE accounts")
        cursor.execute("TRUNCATE TABLE customers")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        self.connection.commit()
        
        # Create test customer
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
    
    def tearDown(self):
        """Clean up after test"""
        db.close()
    
    def test_customer_creation(self):
        """Test creating a customer"""
        # Retrieve the customer we created in setUp
        retrieved_customer = Customer.get_by_email("test@example.com")
        
        self.assertIsNotNone(retrieved_customer)
        self.assertEqual(retrieved_customer.first_name, "Test")
        self.assertEqual(retrieved_customer.last_name, "User")
    
    def test_account_creation(self):
        """Test creating an account"""
        # Create a test account
        test_account = Account(
            customer_id=self.test_customer.customer_id,
            account_number="TEST0001234567",
            card_number="5196061234567890",
            card_type="MASTERCARD",
            credit_limit=10000.00,
            current_balance=0.00,
            statement_date=15,
            payment_due_date=5,
            annual_interest_rate=17.90,
            opening_date=date.today()
        )
        test_account.save()
        
        # Retrieve the account
        retrieved_account = Account.get_by_account_number("TEST0001234567")
        
        self.assertIsNotNone(retrieved_account)
        self.assertEqual(retrieved_account.card_type, "MASTERCARD")
        self.assertEqual(float(retrieved_account.credit_limit), 10000.00)
    
    def test_transaction_creation(self):
        """Test creating a transaction"""
        # Create a test account
        test_account = Account(
            customer_id=self.test_customer.customer_id,
            account_number="TEST0001234567",
            card_number="5196061234567890",
            card_type="MASTERCARD",
            credit_limit=10000.00,
            current_balance=0.00,
            statement_date=15,
            payment_due_date=5,
            annual_interest_rate=17.90,
            opening_date=date.today()
        )
        test_account.save()
        
        # Create a test transaction
        test_transaction = Transaction(
            account_id=test_account.account_id,
            transaction_date=datetime.now(),
            posting_date=datetime.now(),
            merchant_name="TEST MERCHANT",
            amount=-150.00,
            description="Test purchase",
            transaction_type="PURCHASE",
            currency="MYR"
        )
        test_transaction.save()
        
        # Retrieve transactions for account
        transactions = Transaction.get_by_account_id(test_account.account_id)
        
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].merchant_name, "TEST MERCHANT")
        self.assertEqual(float(transactions[0].amount), -150.00)
    
    def test_account_balance_update(self):
        """Test updating account balance with transactions"""
        # Create a test account
        test_account = Account(
            customer_id=self.test_customer.customer_id,
            account_number="TEST0001234567",
            card_number="5196061234567890",
            card_type="MASTERCARD",
            credit_limit=10000.00,
            current_balance=0.00,
            statement_date=15,
            payment_due_date=5,
            annual_interest_rate=17.90,
            opening_date=date.today()
        )
        test_account.save()
        
        # Create purchase transaction
        purchase_transaction = Transaction(
            account_id=test_account.account_id,
            transaction_date=datetime.now(),
            posting_date=datetime.now(),
            merchant_name="TEST MERCHANT",
            amount=-500.00,
            description="Test purchase",
            transaction_type="PURCHASE",
            currency="MYR"
        )
        purchase_transaction.save()
        
        # Update account balance
        purchase_transaction.update_account_balance()
        
        # Retrieve updated account
        updated_account = Account.get_by_id(test_account.account_id)
        self.assertEqual(float(updated_account.current_balance), 500.00)
        
        # Create payment transaction
        payment_transaction = Transaction(
            account_id=test_account.account_id,
            transaction_date=datetime.now(),
            posting_date=datetime.now(),
            merchant_name="CIMB PAYMENT",
            amount=200.00,
            description="Test payment",
            transaction_type="PAYMENT",
            currency="MYR"
        )
        payment_transaction.save()
        
        # Update account balance
        payment_transaction.update_account_balance()
        
        # Retrieve updated account
        updated_account = Account.get_by_id(test_account.account_id)
        self.assertEqual(float(updated_account.current_balance), 300.00)

if __name__ == "__main__":
    unittest.main()