import csv
import unittest
from main_files.databaseconn_main import *
from src.CSVReader.functions_transformation import *
from src.load_to_redshift import *

# load_dotenv('database/.env')  # load environment variables from .env file

# # Get the path of the current file
# current_file_path = os.path.dirname(__file__)

# # create a database connnection
# conn, cursor = database_connection(dbname, user, password, host, port)

# class TestDatabase(unittest.TestCase):
    
#     def setUp(self):
#         # connect to the database
#         self.conn = psycopg2.connect(
#         dbname=dbname,
#         user=user,
#         password=password,
#         host=host,
#         port=port
#         )
        
#     def tearDown(self):
#         # close the database connection
#         self.conn.close()
        
#     def test_branches_populated(self):
#         cur = self.conn.cursor()
#         cur.execute("SELECT COUNT(*) FROM branches")
#         count = cur.fetchone()[0]
#         cur.close()
#         self.assertTrue(count > 0)
        
#     def test_orders_populated(self):
#         cur = self.conn.cursor()
#         cur.execute("SELECT COUNT(*) FROM orders")
#         count = cur.fetchone()[0]
#         cur.close()
#         self.assertTrue(count > 0)
        
#     def test_payments_populated(self):
#         cur = self.conn.cursor()
#         cur.execute("SELECT COUNT(*) FROM payments")
#         count = cur.fetchone()[0]
#         cur.close()
#         self.assertTrue(count > 0)
        
#     def test_products_populated(self):
#         cur = self.conn.cursor()
#         cur.execute("SELECT COUNT(*) FROM products")
#         count = cur.fetchone()[0]
#         cur.close()
#         self.assertTrue(count > 0)
        
#     def test_database_connection(self):
#         self.assertIsNotNone(self.conn)
        
class TestSplitIntoOrder(unittest.TestCase):

    def test_split_into_order_single_order(self):
        input_data = [[1, '05/05/2012 09:00', 'Mochafield', 'Large Flavoured latte - Hazelnut - 2.85', 13.0]]
        column_numbers = 3
        expected_output =  [[1, '05/05/2012 09:00', 'Mochafield', 'Large Flavoured latte - Hazelnut - 2.85', 1, 13.0]]
        self.assertEqual(split_into_order(input_data, column_numbers), expected_output)

    def test_split_into_order_multiple_orders(self):
        input_data = [[1, '05/05/2012 09:00',  'Mochafield', 'Large Flavoured latte - Hazelnut - 2.85, Regular Flat white - 2.15', 13.0]]
        column_numbers = 3
        expected_output = [[1, '05/05/2012 09:00', 'Mochafield', 'Large Flavoured latte - Hazelnut - 2.85', 1, 13.0],
                           [1, '05/05/2012 09:00', 'Mochafield', 'Regular Flat white - 2.15', 1, 13.0]]
        self.assertEqual(split_into_order(input_data, column_numbers), expected_output)


class TestSplitSizeAsColumn(unittest.TestCase):

    def test_split_size_as_column_single_order(self):
        input_data = [[1, '05/05/2012 09:00', 'Mochafield', 'Large Flavoured latte - Hazelnut - 2.85', 1, 13.0]]
        column_number = 3
        expected_output = [[1, '05/05/2012 09:00', 'Mochafield', 'Flavoured latte - Hazelnut - 2.85', 'Large', 1, 13.0]]

class TestSplitUnitPriceAsColumn(unittest.TestCase):

    def test_split_unitprice_as_column_single_order(self):
        input_data = [[1, '05/05/2012 09:00', 'Mochafield', 'Flavoured latte - Hazelnut - 2.85', 'Large', 1, 13.0]]
        column_numbers = 3
        expected_output = [[1, '05/05/2012 09:00', 'Mochafield', 'Flavoured latte - Hazelnut', 'Large', 2.85, 1, 13.0]]
        output = split_unitprice_as_column(input_data, column_numbers)
        self.assertEqual(output, expected_output)

    def test_split_unitprice_as_column_multiple_orders(self):
        input_data = [[1, '05/05/2012 09:00', 'Mochafield', 'Flavoured latte - Hazelnut - 2.85', 'Large', 1, 13.0],
                      [1, '05/05/2012 09:00', 'Mochafield', 'Flavoured latte - Vanila - 2.75', 'Large', 1, 13.0]]
        column_numbers = 3
        expected_output = [[1, '05/05/2012 09:00', 'Mochafield', 'Flavoured latte - Hazelnut', 'Large', 2.85, 1, 13.0],
                           [1, '05/05/2012 09:00', 'Mochafield', 'Flavoured latte - Vanila', 'Large', 2.75, 1, 13.0]]
        output = split_unitprice_as_column(input_data, column_numbers)
        self.assertEqual(output, expected_output)

class TestSplitOrdertimeAsColumn(unittest.TestCase):
    
    def test_split_ordertime_as_column(self):
        input_data = [[1, '05/05/2012 09:00', 'Mochafield', 'Flavoured latte - Hazelnut', 'Large', 2.85, 1, 13.0],
                      [1, '05/05/2012 09:00', 'Mochafield', 'Flavoured latte - Vanila', 'Large', 2.75, 1, 13.0]]
        column_number = 1
        expected_output = [[1, '05/05/2012', '09:00', 'Mochafield', 'Flavoured latte - Hazelnut', 'Large', 2.85, 1, 13.0],
                           [1, '05/05/2012', '09:00', 'Mochafield', 'Flavoured latte - Vanila', 'Large', 2.75, 1, 13.0]]
        self.assertEqual(split_ordertime_as_column(input_data, column_number), expected_output)
    
    def test_split_ordertime_as_column_exception(self):
        input_data = [['25/08/2021','Chesterfield', 'Richard']]
        column_number = 0
        with self.assertRaises(Exception):
            split_ordertime_as_column(input_data, column_number)

class TestTransformBranchFile(unittest.TestCase):

    def transform_branch_file(self):
        file_path = 'test/dummy.csv'
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            csv_list = list(reader)
        transform_data = transform_branch_file(csv_list)
        expected_output = [[1, '25/04/2021', '23:10', 'Mochafield', 'Flavoured iced latte - Caramel', 'Large', 3.25, 12.95,'CASH'],
                        [1, '25/04/2021', '23:10', 'Mochafield', 'Flat white', 'Regular', 2.15, 12.95,'CASH'],
                        [1, '25/04/2021', '23:10', 'Mochafield', 'Latte', 'Regular', 2.15, 12.95,'CASH'],
                        [1, '25/04/2021', '23:10', 'Mochafield', 'Flavoured iced latte - Hazelnut', 'Large', 3.25, 12.95, 'CASH'],
                        [1, '25/04/2021', '23:10', 'Mochafield', 'Flat white', 'Regular', 2.15, 12.95,'CASH'],
                        [2, '25/04/2021', '23:12', 'Mochafield', 'Flavoured latte - Hazelnut', 'Large', 2.85, 17.4, 'CARD'],
                        [2, '25/04/2021', '23:12', 'Mochafield', 'Flavoured iced latte - Vanilla', 'Regular', 2.75, 17.4, 'CARD'],
                        [2, '25/04/2021', '23:12', 'Mochafield', 'Flavoured iced latte - Hazelnut', 'Large', 3.25, 17.4, 'CARD'],
                        [2, '25/04/2021', '23:12', 'Mochafield', 'Flavoured iced latte - Vanilla', 'Large', 3.25, 17.4, 'CARD'],
                        [2, '25/04/2021', '23:12', 'Mochafield', 'Latte', 'Large', 2.45, 17.4, 'CARD']]

        self.assertEqual(transform_data, expected_output)

if __name__ == '__main__':
    unittest.main()