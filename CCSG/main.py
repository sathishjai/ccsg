#!/usr/bin/env python3
"""
Credit Card Statement Generator
Main application entry point that coordinates the statement generation process.
"""
import os
import argparse
import logging
from datetime import datetime
from pathlib import Path
from utils.config import Config
from database.connection import DatabaseConnection
from models.customer import Customer
from models.account import Account
from models.transaction import Transaction
from processors.financial_calculator import FinancialCalculator
from processors.data_processor import DataProcessor
from pdf_generator.pdf_builder import PDFBuilder
from pdf_generator.template_manager import TemplateManager
#from utils.config import Config
#from utils.error_handler import setup_error_handling
#from utils.language import get_language_text
config = Config('config.json')  # Pass the filename if needed


def setup_logging():
    """Configure logging for the application."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"statement_generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate credit card statements')
    parser.add_argument('--config', type=str, default='config.ini', help='Path to configuration file')
    parser.add_argument('--customer-id', type=int, help='Generate statement for specific customer ID')
    parser.add_argument('--account-id', type=int, help='Generate statement for specific account ID')
    parser.add_argument('--statement-date', type=str, help='Statement date (YYYY-MM-DD)')
    parser.add_argument('--output-dir', type=str, default='statements', help='Output directory for statements')
    parser.add_argument('--bank-template', type=str, help='Specific bank template to use')
    parser.add_argument('--language', type=str, default='en', help='Language for statements (e.g., en, es, fr)')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    
    return parser.parse_args()


def generate_statement(db_conn, customer_id, account_id, statement_date, output_dir, bank_template, language):
    """Generate a credit card statement for the specified account."""
    logger = logging.getLogger(__name__)
    
    # Get customer data
    customer = Customer.get_by_id(db_conn, customer_id)
    if not customer:
        logger.error(f"Customer {customer_id} not found")
        return False
    
    # Get account data
    account = Account.get_by_id(db_conn, account_id)
    if not account:
        logger.error(f"Account {account_id} not found")
        return False
    
    # Verify account belongs to customer
    if account.customer_id != customer_id:
        logger.error(f"Account {account_id} does not belong to customer {customer_id}")
        return False
    
    # Get transactions for the statement period
    transactions = Transaction.get_for_statement(db_conn, account_id, statement_date)
    
    # Process financial data
    calculator = FinancialCalculator()
    processor = DataProcessor()
    
    statement_data = processor.prepare_statement_data(
        customer, 
        account, 
        transactions, 
        statement_date
    )
    
    # Calculate financial summaries
    statement_data = calculator.calculate_statement_totals(statement_data)
    statement_data = calculator.calculate_interest(statement_data)
    statement_data = calculator.calculate_minimum_payment(statement_data)
    
    # Apply language translations
    statement_data['language_text'] = get_language_text(language)
    
    # Generate PDF statement
    template_manager = TemplateManager()
    template = template_manager.get_template(bank_template or account.bank_name)
    
    pdf_builder = PDFBuilder(template)
    pdf_path = pdf_builder.generate_pdf(statement_data, output_dir)
    
    logger.info(f"Generated statement for account {account_id} at {pdf_path}")
    return pdf_path


def main():
    """Main entry point for the credit card statement generator."""
    # Setup
    logger = setup_logging()
    args = parse_arguments()
    
    # Load configuration
    config = Config(args.config)
    
    # Setup error handling
    setup_error_handling()
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    try:
        # Initialize database connection
        db_conn = DatabaseConnection(
            config.get('database', 'host'),
            config.get('database', 'port', type=int),
            config.get('database', 'database'),
            config.get('database', 'user'),
            config.get('database', 'password')
        )
        
        statement_date = args.statement_date or datetime.now().strftime("%Y-%m-%d")
        
        if args.test:
            logger.info("Running in test mode")
            # Run test generation with sample data
            from tests.test_cases import get_test_cases
            test_cases = get_test_cases()
            
            for test_case in test_cases:
                generate_statement(
                    db_conn,
                    test_case['customer_id'],
                    test_case['account_id'],
                    test_case['statement_date'],
                    args.output_dir,
                    test_case.get('bank_template'),
                    args.language
                )
        elif args.customer_id and args.account_id:
            # Generate a specific statement
            generate_statement(
                db_conn,
                args.customer_id,
                args.account_id,
                statement_date,
                args.output_dir,
                args.bank_template,
                args.language
            )
        else:
            # Generate statements for all accounts due for statements
            accounts_due = Account.get_accounts_due_for_statements(db_conn, statement_date)
            logger.info(f"Generating statements for {len(accounts_due)} accounts")
            
            for account in accounts_due:
                generate_statement(
                    db_conn,
                    account.customer_id,
                    account.id,
                    statement_date,
                    args.output_dir,
                    args.bank_template or account.bank_name,
                    args.language
                )
                
        logger.info("Statement generation completed successfully")
        
    except Exception as e:
        logger.exception(f"Error during statement generation: {e}")
        return 1
    finally:
        if 'db_conn' in locals():
            db_conn.close()
    
    return 0


import logging
from config import Config

def main():
    try:
        # Initialize Config object
        config = Config('config.json')  # Specify the config file if needed
        print(config.get_config())  # Or do something with the config
    except ConfigurationError as e:
        logging.error(f"Failed to load configuration: {str(e)}")
        exit(1)




if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)