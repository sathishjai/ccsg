from models.customer import Customer
from models.account import Account
from models.transaction import Transaction

class DataProcessor:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_customer_data(self, customer_id):
        query = """
            SELECT * FROM customers 
            WHERE customer_id = ?
        """
        result = self.db.execute_query(query, (customer_id,))
        if result:
            return Customer(**dict(result[0]))
        return None

    def get_account_data(self, customer_id):
        query = """
            SELECT * FROM accounts 
            WHERE customer_id = ?
        """
        result = self.db.execute_query(query, (customer_id,))
        if result:
            return Account(**dict(result[0]))
        return None

    def get_transactions(self, customer_id, statement_date):
        query = """
            SELECT t.* FROM transactions t
            JOIN accounts a ON t.account_id = a.account_id
            WHERE a.customer_id = ? 
            AND strftime('%Y-%m', t.transaction_date) = ?
            ORDER BY t.transaction_date DESC
        """
        results = self.db.execute_query(query, (customer_id, statement_date))
        return [Transaction(**dict(row)) for row in results]