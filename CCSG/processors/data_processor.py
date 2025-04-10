from models.customer import Customer
from models.account import Account
from models.transaction import Transaction
from processors.financial_calculator import FinancialCalculator
from utils.error_handler import DataProcessingError
import logging

class DataProcessor:
    """Processes data for credit card statement generation"""
    
    def __init__(self, db_connection):
        """
        Initialize data processor with database connection
        
        Args:
            db_connection: Database connection object
        """
        self.db = db_connection
        self.calculator = FinancialCalculator()
    
    def process_statement_data(self, customer_id, statement_date=None):
        """
        Process all data needed for statement generation
        
        Args:
            customer_id: ID of the customer
            statement_date: Optional statement date (defaults to most recent)
            
        Returns:
            Dictionary with all processed data for statement generation
        """
        try:
            # Get customer and account data
            customer_data = self.db.get_customer_data(customer_id)
            
            if not customer_data:
                raise DataProcessingError(f"No data found for customer ID: {customer_id}")
            
            # Create models from database data
            customer = Customer(customer_data[0])
            account = Account(customer_data[0])
            
            # Get statement period
            statement_period = account.get_statement_period(statement_date)
            
            # Get transactions for the period
            transactions_data = self.db.get_transactions(
                account.account_number,
                statement_period['start_date'],
                statement_period['end_date']
            )
            
            transactions = [Transaction(t) for t in transactions_data]
            
            # Get rewards data
            rewards_data = self.db.get_rewards(account.account_number)
            rewards = rewards_data[0] if rewards_data else {}
            
            # Calculate statement summary
            summary = self.calculator.calculate_statement_summary(transactions)
            
            # Categorize transactions
            categorized_transactions = self._categorize_transactions(transactions)
            
            # Prepare final statement data
            statement_data = {
                'customer': customer.to_dict(),
                'account': account.to_dict(),
                'statement_period': statement_period,
                'transactions': [t.to_dict() for t in transactions],
                'categorized_transactions': categorized_transactions,
                'summary': summary,
                'rewards': rewards,
                'language': account.language_preference
            }
            
            return statement_data
            
        except Exception as e:
            logging.error(f"Error processing statement data: {str(e)}")
            raise DataProcessingError(f"Failed to process statement data: {str(e)}")
    
    def _categorize_transactions(self, transactions):
        """
        Categorize transactions by type for easier processing in templates
        
        Args:
            transactions: List of transaction objects
            
        Returns:
            Dictionary with transactions organized by category
        """
        categories = {
            'payments': [],
            'purchases': [],
            'fees': [],
            'interest': [],
            'other': []
        }
    def _categorize_transactions(self, transactions):
        """
        Categorize transactions by type for easier processing in templates
        
        Args:
            transactions: List of transaction objects
            
        Returns:
            Dictionary with transactions organized by category
        """
        categories = {
            'payments': [],
            'purchases': [],
            'fees': [],
            'interest': [],
            'other': []
        }
        
        for transaction in transactions:
            if transaction.transaction_type == 'Payment':
                categories['payments'].append(transaction)
            elif transaction.transaction_type == 'Purchase':
                categories['purchases'].append(transaction)
            elif transaction.transaction_type == 'Fee':
                categories['fees'].append(transaction)
            elif transaction.transaction_type == 'Interest':
                categories['interest'].append(transaction)
            else:
                categories['other'].append(transaction)
        
        return categories
