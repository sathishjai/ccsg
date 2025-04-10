import unittest
import os
from pdf_generator.pdf_builder import PDFBuilder
from models.customer import Customer
from models.account import Account
from models.transaction import Transaction

class TestPDFGeneration(unittest.TestCase):
    def setUp(self):
        self.pdf_builder = PDFBuilder()
        
        # Create test data
        self.customer = Customer(
            customer_id=1,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="555-0123",
            address="123 Main St",
            city="Anytown",
            state="ST",
            zip_code="12345"
        )
        
        self.account = Account(
            account_id=1,
            customer_id=1,
            account_number="4111111111111111",
            card_number="************1111",
            credit_limit=5000.00,
            current_balance=1250.00,
            statement_date="2023-01-31",
            due_date="2023-02-25"
        )
        
        self.transactions = [
            Transaction(1, 1, "2023-01-15", "2023-01-15", "Grocery Store", 75.50, "Groceries"),
            Transaction(2, 1, "2023-01-16", "2023-01-16", "Gas Station", 45.00, "Auto"),
            Transaction(3, 1, "2023-01-20", "2023-01-20", "Payment", -100.00, "Payment")
        ]

    def test_pdf_generation(self):
        # Test PDF generation
        output_file = self.pdf_builder.generate_statement(
            self.customer,
            self.transactions,
            "2023-01"
        )
        
        # Check if file was created
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(os.path.getsize(output_file) > 0)
        
        # Cleanup
        os.remove(output_file)

    def test_template_loading(self):
        # Test template manager
        template = self.pdf_builder.template_manager.get_template('default')
        self.assertIsNotNone(template)