import pymysql
from utils.error_handler import ErrorHandler

class DatabaseConnection:
    def __init__(self, db_config):
        self.host = db_config.get('host', 'localhost')
        self.user = db_config.get('user', 'root')
        self.password = db_config.get('password', '2001')
        self.database = db_config.get('database', 'credit_card_db')
        self.port = db_config.get('port', 3306)
        self.connection = None
        
    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                cursorclass=pymysql.cursors.DictCursor
            )
            return self.connection
        except Exception as e:
            ErrorHandler.handle_error(f"Database connection error: {str(e)}")
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            
    def execute_query(self, query, params=None):
        try:
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    if query.strip().upper().startswith(('SELECT', 'SHOW')):
                        return cursor.fetchall()
                    conn.commit()
                    return cursor.rowcount
        except Exception as e:
            ErrorHandler.handle_error(f"Query execution error: {str(e)}")