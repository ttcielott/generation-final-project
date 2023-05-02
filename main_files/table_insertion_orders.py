import os
from dotenv import load_dotenv
from main_files.databaseconn_main import *
from main_files.functions_main import *
from datetime import datetime

 # load environment variables from .env file
load_dotenv('database/.env') 

# create a database connnection
conn, cursor = database_connection(dbname, user, password, host, port)

# get csv file paths and save them as a list
csv_files = get_csv_files_path()

def load_order_data(order_data):

    for order in order_data:
        branch_id = order["branch_id"]
        payment_method_id = order["payment_method_id"]
        total_order_amount = order["total_order_amount"]
        order_date = order["order_date"]
        order_time = order["order_time"]

        cursor.execute(
            """
            INSERT INTO orders
            (branch_id, payment_method_id, total_order_amount, order_date, order_time)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (branch_id, payment_method_id, total_order_amount, order_date, order_time)
        )
def load_order_product_data(order_product_data):
    
    for order_product in order_product_data:
        order_id = order_product["order_id"]
        product_id = order_product["product_id"]
        order_qty = order_product["order_qty"]

        cursor.execute(
            """
            INSERT INTO order_product
            (order_id, product_id, order_qty)
            VALUES (%s, %s, %s)
            """,
            (order_id, product_id, order_qty)
        )

# loop through the csv file path
for file_path in csv_files: 

    # extract raw csv file without the column, customer name and credit card number
    transformed_data1 = extract_without(file_path, [2, 6])

    # split the column, datetime into date and time
    transformed_data2 = split_ordertime_as_column(transformed_data1, 0)

    for row in transformed_data2:
       
        branch_name = row[1]
        payment_method = row[4]
        total_order_amount = row[3]
        order_date = row[0]
        order_date = datetime.strptime(order_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        order_time = row[5]

        sql_branch = """SELECT branch_id
                        FROM branches
                        WHERE branch_name = %s 
                     """
        sql_payment = """SELECT payment_method_id
                         FROM payments
                         WHERE payment_method_name = %s
                      """
        
        branch_values = (branch_name,)
        cursor.execute(sql_branch, branch_values)
        Branch_id = cursor.fetchone()[0]

        payment_values = (payment_method,)
        cursor.execute(sql_payment, payment_values)
        Payment_method_id = cursor.fetchone()[0]


        # Define the order data as a list of dictionaries
        order_data = [{"branch_id": Branch_id, 
                   "payment_method_id": Payment_method_id, 
                   "total_order_amount": total_order_amount, 
                   "order_date": order_date, "order_time": order_time}]

        # Call the load_order_data function to insert data into the orders table
        load_order_data(order_data)

         # transform transformed_data2 to split multiple orders in one row into single order in one row
        transformed_data3 = split_into_order([row], 2)

        # query a newly-created order_id
        sql_order = """SELECT MAX(order_id)
                        FROM orders
                    """
        cursor.execute(sql_order)
        Order_id = cursor.fetchone()[0]

        # transform transformed_data3 to split size from order
        transformed_data4 = split_size_as_column(transformed_data3, 2)

        # transform transformed_data4 to split unit price from order
        transformed_data5 = split_unitprice_as_column(transformed_data4, -1)


        for row in transformed_data5:
            
            product_name = row[-2]
            product_size = row[2]
            order_qty = row[-3]

            # Create the sql statement to query order_id and product_id
            sql_product = """SELECT product_id
                            FROM products
                            WHERE product_name = %s
                            AND product_size = %s 
                        """

            product_values = (product_name, product_size)
            cursor.execute(sql_product, product_values)
            Product_id = cursor.fetchone()[0]
            
            # Define the order_product_data as a list of dictionaries
            order_product_data = [{"order_id": Order_id,
                                   "product_id": Product_id, 
                                   "order_qty": order_qty}]

            print(order_product_data)

            # Call the load_order_product_data to insert data into the order_product table
            load_order_product_data(order_product_data)

conn.commit()
cursor.close()
conn.close()