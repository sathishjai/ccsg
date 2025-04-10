import unittest
from database.connection import DatabaseConnection
from utils.config import Config

class TestDatabase(unittest.TestCase):
    def setUp(self):
        config = Config()
        self.db = DatabaseConnection(config.get_db_config())

    def test_connection(self):
        connection = self.db.connect()
        self.assertIsNotNone(connection)
        self.db.disconnect()

    def test_execute_query(self):
        # Test select query
        query = "SELECT * FROM customers LIMIT 1"
        result = self.db.execute_query(query)
        self.assertIsNotNone(result)

    def tearDown(self):
        self.db.disconnect()