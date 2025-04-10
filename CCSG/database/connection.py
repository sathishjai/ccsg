import pyodbc
import logging
#from utils.config import get_db_config
#from utils.error_handler import DatabaseError

class DatabaseConnection:
    """Class to handle database connections and operations"""
    
    def __init__(self):
        """Initialize database connection"""
        self.connection = None
        self.cursor = None
        self.config = get_db_config()
    
    def connect(self):
        """Establish connection to the database"""
        try:
            connection_string = (
                f"DRIVER={{SQL Server}};"
                f"SERVER={self.config['server']};"
                f"DATABASE={self.config['database']};"
                f"UID={self.config['2001']};"
                f"PWD={self.config['2001']};"
            )
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            logging.info("Database connection established successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to database: {str(e)}")
            raise DatabaseError(f"Database connection error: {str(e)}")
    
    def disconnect(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            # If the query is a SELECT statement, return results
            if query.strip().upper().startswith('SELECT'):
                columns = [column[0] for column in self.cursor.description]
                return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            else:
                self.connection.commit()
                return True
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Query execution error: {str(e)}")
            raise DatabaseError(f"Query execution error: {str(e)}")
    
    def get_customer_data(self, customer_id):
        """Get customer information"""
        query = """
        SELECT c.*, a.account_number, a.credit_limit, a.available_credit, 
               a.current_balance, a.statement_date, a.payment_due_date,
               a.minimum_payment, a.previous_balance, a.language_preference
        FROM customers c
        JOIN accounts a ON c.customer_id = a.customer_id
        WHERE c.customer_id = ?
        """
        return self.execute_query(query, (customer_id,))
    
    def get_transactions(self, account_number, start_date, end_date):
        """Get transactions for a specific period"""
        query = """
        SELECT t.transaction_id, t.transaction_date, t.posting_date,
               t.description, t.amount, t.transaction_type, t.mcc_code,
               t.reference_number
        FROM transactions t
        WHERE t.account_number = ?
        AND t.posting_date BETWEEN ? AND ?
        ORDER BY t.posting_date DESC, t.transaction_id DESC
        """
        return self.execute_query(query, (account_number, start_date, end_date))
    
    def get_rewards(self, account_number):
        """Get rewards information for an account"""
        query = """
        SELECT r.rewards_id, r.points_earned, r.points_redeemed,
               r.points_balance, r.points_expiring, r.expiry_date
        FROM rewards r
        WHERE r.account_number = ?
        """
        return self.execute_query(query, (account_number,))
