import os
from dotenv import load_dotenv
from main_files.databaseconn_main import *
from main_files.functions_main import *
from dotenv import load_dotenv

load_dotenv('database/.env')  # load environment variables from .env file

# Get the path of the current file
current_file_path = os.path.dirname(__file__)

# create a database connnection
conn, cursor = database_connection(dbname, user, password, host, port)

# Navigate to the data folder
data_folder = "csv_files"

# Get a list of all CSV files in the data folder
csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]

# loop through the csv file path
for file_path in csv_files:
    transformed_data = transform_branch_file(file_path)
    
    Customer_id = 0
    for row in transformed_data:
        Branch_name = row[1]
        Product_name = row[-3]
        Size = row[-6]


        sql = """SELECT product_id
                  FROM products
                  WHERE product_name = %s
                  AND product_size = %s
               """
    
        data_values = (Product_name, Size)
        cursor.execute(sql, data_values)
        Product_id = cursor.fetchone()[0]
        print(Product_id)

    


def fetch_product_branch_payment_data():
    cursor = conn.cursor()

    cursor.execute("SELECT product_id, product_name, product_size, product_price FROM products")
    products = cursor.fetchall()

    cursor.execute("SELECT branch_id, branch_name FROM branches")
    branches = cursor.fetchall()

    cursor.execute("SELECT payment_method_id, payment_method_name FROM payments")
    payments = cursor.fetchall()

    cursor.close()
    conn.close()

    return products, branches, payments

def load_order_data(order_data):
    cursor = conn.cursor()

    for order in order_data:
        branch_id = order["branch_id"]
        product_id = order["product_id"]
        payment_method_id = order["payment_method_id"]
        total_order_amount = order["total_order_amount"]
        order_date = order["order_date"]
        order_time = order["order_time"]

        cursor.execute(
            """
            INSERT INTO orders
            (branch_id, product_id, payment_method_id, total_order_amount, order_date, order_time)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (branch_id, product_id, payment_method_id, total_order_amount, order_date, order_time)
        )

    conn.commit()
    cursor.close()
    conn.close()