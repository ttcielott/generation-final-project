import os
from dotenv import load_dotenv
from main_files.databaseconn_main import *
from main_files.functions_main import *
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('database/.env')  # load environment variables from .env file

# Get the path of the current file
current_file_path = os.path.dirname(__file__)

# create a database connnection
conn, cursor = database_connection(dbname, user, password, host, port)

# Navigate to the data folder
data_folder = "csv_files"

# Get a list of all CSV files in the data folder
csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]

def load_order_data(order_data):
    cursor = conn.cursor()

    for order in order_data:
        branch_id = order["branch_id"]
        product_id = order["product_id"]
        payment_method_id = order["payment_method_id"]
        total_order_amount = order["total_order_amount"]
        order_date = datetime.strptime(order["order_date"], '%d/%m/%Y').strftime('%Y-%m-%d')
        order_time = order["order_time"]

        cursor.execute(
            """
            INSERT INTO orders
            (branch_id, product_id, payment_method_id, total_order_amount, order_date, order_time)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (branch_id, product_id, payment_method_id, total_order_amount, order_date, order_time)
        )

# loop through the csv file path
for file_path in csv_files:
    transformed_data = transform_branch_file(file_path)
    
    for row in transformed_data:
        branch_name = row[1]
        product_name = row[6]
        product_size = row[3]
        payment_method = row[5]
        total_order_amount = row[4]
        order_date = row[0]
        order_time = row[8]

        sql_product = """SELECT product_id
                         FROM products
                         WHERE product_name = %s
                         AND product_size = %s 
                      """
        sql_branch = """SELECT branch_id
                        FROM branches
                        WHERE branch_name = %s 
                     """
        sql_payment = """SELECT payment_method_id
                         FROM payments
                         WHERE payment_method_name = %s
                      """
        
        data_values1 = (product_name, product_size)
        cursor.execute(sql_product, data_values1)
        Product_id = cursor.fetchone()[0]

        data_values2 = (branch_name,)
        cursor.execute(sql_branch, data_values2)
        Branch_id = cursor.fetchone()[0]

        data_values3 = (payment_method,)
        cursor.execute(sql_payment, data_values3)
        Payment_method_id = cursor.fetchone()[0]

        print(Product_id, Branch_id, Payment_method_id)

        # Define the order data as a list of dictionaries
        order_data = [    {"branch_id": Branch_id, 
                   "product_id": Product_id, 
                   "payment_method_id": Payment_method_id, 
                   "total_order_amount": total_order_amount, 
                   "order_date": order_date, "order_time": order_time}]

        # Call the load_order_data function to insert data into the orders table
        load_order_data(order_data)

conn.commit()
cursor.close()
conn.close()