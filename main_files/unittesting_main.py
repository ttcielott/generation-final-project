import os
import unittest
import psycopg2
from dotenv import load_dotenv
from main_files.databaseconn_main import *
from main_files.functions_main import *
from main_files.functions_main import split_into_order, split_size_as_column, split_unitprice_as_column, split_ordertime_as_column, transform_branch_file
from dotenv import load_dotenv
from typing import List

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
        
class TestSplitIntoOrder(unittest.TestCase):

    def test_split_into_order_single_order(self):
        input_data = [['tom', 'Large Flavoured latte - Hazelnut - 2.85', 13.0]]
        column_numbers = [1]
        expected_output = [['tom', 'Large Flavoured latte - Hazelnut - 2.85', 13.0]]
        self.assertEqual(split_into_order(input_data, column_numbers[0]), expected_output)

    def test_split_into_order_multiple_orders(self):
        input_data = [['tom', 'Large Flavoured latte - Hazelnut - 2.85, Regular Flat white - 2.15', 13.0]]
        column_numbers = [1]
        expected_output = [['tom', 'Large Flavoured latte - Hazelnut - 2.85', 13.0],
                           ['tom', 'Regular Flat white - 2.15', 13.0]]
        self.assertEqual(split_into_order(input_data, column_numbers[0]), expected_output)


class TestSplitSizeAsColumn(unittest.TestCase):

    def test_split_size_as_column_single_order(self):
        input_data = [['tom', 'Flavoured latte - Hazelnut - 2.85', 13.0]]
        column_numbers = [1]
        expected_output = [['tom', 'Flavoured latte - Hazelnut - 2.85', 13.0]]
        self.assertEqual(split_size_as_column(input_data, column_numbers[0]), expected_output)

    def test_split_size_as_column_multiple_orders(self):
        input_data = [['tom', 'Large Flavoured latte - Hazelnut - 2.85', 13.0, 'Large'],
                      ['tom', 'Regular Flat white - 2.15', 13.0, 'Regular']]
        column_numbers = [1]
        expected_output = [['tom', 'Flavoured latte - Hazelnut - 2.85', 13.0, 'Large'],
                           ['tom', 'Flat white - 2.45', 13.0, 'Regular']]
        self.assertEqual(split_size_as_column(input_data, column_numbers[0]), expected_output)

class TestSplitUnitPriceAsColumn(unittest.TestCase):

    def test_split_unitprice_as_column_single_order(self):
        input_data = [['tom', 'Flavoured latte - Hazelnut - 2.85', 13.0, 'Large']]
        column_numbers = [1]
        expected_output = [['tom', 'Flavoured latte - Hazelnut', 13.0, 'Large', 2.85]]
        self.assertEqual(split_unitprice_as_column(input_data, column_numbers[0]), expected_output)

    def test_split_unitprice_as_column_multiple_orders(self):
        input_data = [['tom', 'Flavoured latte - Hazelnut - 2.85', 13.0, 'Large'],
                      ['tom', 'Flat white - 2.45', 13.0, 'Regular']]
        column_numbers = [1]
        expected_output = [['tom', 'Flavoured latte - Hazelnut', 13.0, 'Large', 2.85],
                           ['tom', 'Flat white', 13.0, 'Regular', 2.45]]
        self.assertEqual(split_unitprice_as_column(input_data, column_numbers[0]), expected_output)

class TestSplitOrdertimeAsColumn(unittest.TestCase):
    
    def test_split_ordertime_as_column(self):
        input_data = [['25/08/2021 09:00','Chesterfield', 'Richard']]
        column_number = 0
        expected_output = [['25/08/2021','Chesterfield', 'Richard', '09:00']]
        self.assertEqual(split_ordertime_as_column(input_data, column_number), expected_output)
    
    def test_split_ordertime_as_column_exception(self):
        input_data = [['25/08/2021','Chesterfield', 'Richard']]
        column_number = 0
        with self.assertRaises(Exception):
            split_ordertime_as_column(input_data, column_number)

class TestTransformBranchFile(unittest.TestCase):

    def test_transform_branch_file(self):
        file_path = 'csv_files/chesterfield_25-08-2021_09-00-00.csv'
        expected_output = [['25/08/2021', 'Chesterfield', 'Richard', 'Small', '2.5', 'CASH', 'Cappuccino', '09:00']]
        self.assertEqual(transform_branch_file(file_path), expected_output)
        
    def test_get_csv_files_path(self):
        expected_output = ['csv_files\\chesterfield_25-08-2021_09-00-00.csv', 'csv_files\\leeds_01-01-2020_09-00-00.csv', 'csv_files\\london_soho_26.04.2023_09-00-00.csv']
        self.assertEqual(get_csv_files_path(), expected_output)

if __name__ == '__main__':
    unittest.main()