import os
import unittest
import psycopg2
from dotenv import load_dotenv
from main_files.databaseconn_main import *
from main_files.functions_main import *
from dotenv import load_dotenv

load_dotenv('database/.env')  # load environment variables from .env file

# Get the path of the current file
current_file_path = os.path.dirname(__file__)

# create a database connnection
conn, cursor = database_connection(dbname, user, password, host, port)

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        # connect to the database
        self.conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
        )
        
    def tearDown(self):
        # close the database connection
        self.conn.close()
        
    def test_branches_populated(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM branches")
        count = cur.fetchone()[0]
        cur.close()
        self.assertTrue(count > 0)
        
    def test_orders_populated(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM orders")
        count = cur.fetchone()[0]
        cur.close()
        self.assertTrue(count > 0)
        
    def test_payments_populated(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM payments")
        count = cur.fetchone()[0]
        cur.close()
        self.assertTrue(count > 0)
        
    def test_products_populated(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM products")
        count = cur.fetchone()[0]
        cur.close()
        self.assertTrue(count > 0)
        
    def test_database_connection(self):
        self.assertIsNotNone(self.conn)
        
if __name__ == '__main__':
    unittest.main()