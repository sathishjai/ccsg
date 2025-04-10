# tests/test_calculations.py
import unittest
import os
import sys
from datetime import datetime, date, timedelta
from decimal import Decimal

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processors.financial_calculator import FinancialCalculator
from models.customer import Customer
from models.account import Account
from models.transaction import Transaction
from database.connection import db

class TestFinancialCalculations(unittest.TestCase):
    """Test financial calculations for credit card statements"""
    
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
            current_balance=0.00,
            statement_date=15,
            payment_due_date=10,
            annual_interest_rate=18.00,
            opening_date=date.today() - timedelta(days=90)
        )
        self.test_account.save()
        
        # Create the financial calculator
        self.calculator = FinancialCalculator()
    
    def tearDown(self):
        """Clean up after test"""
        db.close()
    
    def test_minimum_payment_calculation(self):
        """Test minimum payment calculation"""
        # Test with various balances
        self.assertEqual(self.calculator.calculate_minimum_payment(100), 10)  # 10% of small balance
        self.assertEqual(self.calculator.calculate_minimum_payment(500), 50)  # 10% of balance
        self.assertEqual(self.calculator.calculate_minimum_payment(5000), 250)  # 5% for larger balance
        
        # Test minimum payment floor
        self.assertEqual(self.calculator.calculate_minimum_payment(50), 10)  # Minimum payment is 10
    
    def test_interest_calculation(self):
        """Test interest calculation"""
        # Create transactions for testing
        for i in range(1, 6):
            # Create purchase transactions across statement period
            days_ago = 45 - (i * 5)  # Spread transactions across statement period
            transaction_date = date.today() - timedelta(days=days_ago)
            
            transaction = Transaction(
                account_id=self.test_account.account_id,
                transaction_date=datetime.combine(transaction_date, datetime.min.time()),
                posting_date=datetime.combine(transaction_date + timedelta(days=1), datetime.min.time()),
                merchant_name=f"TEST MERCHANT {i}",
                amount=-500.00,  # 500 per transaction
                description=f"Test purchase {i}",
                transaction_type="PURCHASE",
                currency="MYR"
            )
            transaction.save()
            transaction.update_account_balance()
        
        # Make a payment 20 days ago
        payment_date = date.today() - timedelta(days=20)
        payment = Transaction(
            account_id=self.test_account.account_id,
            transaction_date=datetime.combine(payment_date, datetime.min.time()),
            posting_date=datetime.combine(payment_date, datetime.min.time()),
            merchant_name="CIMB PAYMENT",
            amount=1000.00,  # 1000 payment
            description="Test payment",
            transaction_type="PAYMENT",
            currency="MYR"
        )
        payment.save()
        payment.update_account_balance()
        
        # Retrieve updated account
        self.test_account = Account.get_by_id(self.test_account.account_id)
        
        # Generate a billing cycle
        today = date.today()
        prev_month = today.replace(day=1) - timedelta(days=1)
        start_date = prev_month.replace(day=16)  # 16th of previous month
        end_date = today.replace(day=15)  # 15th of current month
        
        cycle_id = self.calculator.create_billing_cycle(
            self.test_account.account_id,
            start_date,
            end_date
        )
        
        # Calculate interest for the cycle
        interest = self.calculator.calculate_interest(self.test_account.account_id, cycle_id)
        
        # Expected balance: 5*500 - 1000 = 1500
        # Expected interest at 18% APR for a month: ~1500 * 0.18 / 12 = ~22.5
        # But actual calculation will vary based on daily balances
        self.assertGreater(interest, 0)
        
        # Test that interest is recorded in the database
        query = """
            SELECT * FROM interest_calculations 
            WHERE account_id = %s AND cycle_id = %s
        """
        results = db.execute_query(query, (self.test_account.account_id, cycle_id), fetch=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(float(results[0]['principal_amount']), 1500.00)
    
    def test_statement_summary_calculation(self):
        """Test statement summary calculations"""
        # Create initial balance
        self.test_account.current_balance = 1000.00
        self.test_account.save()
        
        # Create some purchases and payments in the statement period
        today = date.today()
        statement_start = today.replace(day=1)
        statement_end = today.replace(day=15) if today.day > 15 else today
        
        # Create 3 purchases
        for i in range(1, 4):
            transaction_date = statement_start + timedelta(days=i * 3)
            if transaction_date <= statement_end:
                transaction = Transaction(
                    account_id=self.test_account.account_id,
                    transaction_date=datetime.combine(transaction_date, datetime.min.time()),
                    posting_date=datetime.combine(transaction_date + timedelta(days=1), datetime.min.time()),
                    merchant_name=f"TEST MERCHANT {i}",
                    amount=-200.00,  # 200 per transaction
                    description=f"Test purchase {i}",
                    transaction_type="PURCHASE",
                    currency="MYR"
                )
                transaction.save()
                transaction.update_account_balance()
        
        # Create 1 payment
        payment_date = statement_start + timedelta(days=10)
        if payment_date <= statement_end:
            payment = Transaction(
                account_id=self.test_account.account_id,
                transaction_date=datetime.combine(payment_date, datetime.min.time()),
                posting_date=datetime.combine(payment_date, datetime.min.time()),
                merchant_name="CIMB PAYMENT",
                amount=300.00,  # 300 payment
                description="Test payment",
                transaction_type="PAYMENT",
                currency="MYR"
            )
            payment.save()
            payment.update_account_balance()
        
        # Create a billing cycle
        cycle_id = self.calculator.create_billing_cycle(
            self.test_account.account_id,
            statement_start,
            statement_end
        )
        
        # Calculate statement summary
        summary = self.calculator.calculate_statement_summary(
            self.test_account.account_id,
            cycle_id
        )
        
        # Check summary calculations
        self.assertEqual(summary['previous_balance'], Decimal('1000.00'))
        
        # Check if number of purchases is correct
        # Note: This may vary based on today's date when running the test
        purchases_in_period = Transaction.get_by_date_range(
            self.test_account.account_id,
            statement_start,
            statement_end,
            "PURCHASE"
        )
        self.assertEqual(summary['total_purchases'], Decimal(abs(sum(float(t.amount) for t in purchases_in_period))))
        
        # Check if number of payments is correct
        payments_in_period = Transaction.get_by_date_range(
            self.test_account.account_id,
            statement_start,
            statement_end,
            "PAYMENT"
        )
        self.assertEqual(summary['total_payments'], Decimal(sum(float(t.amount) for t in payments_in_period)))

if __name__ == "__main__":
    unittest.main()