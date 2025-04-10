import unittest
from processors.financial_calculator import FinancialCalculator
from models.transaction import Transaction

class TestCalculations(unittest.TestCase):
    def test_minimum_payment(self):
        # Test minimum payment calculation
        self.assertEqual(FinancialCalculator.calculate_minimum_payment(1000), 25.00)
        self.assertEqual(FinancialCalculator.calculate_minimum_payment(2000), 40.00)

    def test_interest_calculation(self):
        # Test interest calculation
        balance = 1000
        apr = 0.1499
        interest = FinancialCalculator.calculate_interest(balance, apr)
        self.assertGreater(interest, 0)

    def test_statement_summary(self):
        # Create test transactions
        transactions = [
            Transaction(1, 1, '2023-01-01', '2023-01-01', 'Purchase 1', 100.00, 'Retail'),
            Transaction(2, 1, '2023-01-02', '2023-01-02', 'Payment', -50.00, 'Payment')
        ]
        
        summary = FinancialCalculator.get_statement_summary(transactions)
        self.assertEqual(summary['total_purchases'], 100.00)
        self.assertEqual(summary['total_payments'], 50.00)
        self.assertEqual(summary['transaction_count'], 2)