import pyodbc

def connect_to_db():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=server_name;'
                          'DATABASE=database_name;'
                          'UID=username;'
                          'PWD=password')
    return conn
