import os
from dotenv import load_dotenv
from main_files.databaseconn_main import *
from main_files.functions_main import *
from dotenv import load_dotenv

load_dotenv('database/.env')  # load environment variables from .env file

# create a database connnection
conn, cursor = database_connection(dbname, user, password, host, port)

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