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
    csv_list = read_csv(file_path)

    # transform data
    transformed_data = transform_branch_file(csv_list)

    # set key names
    key_names = ['temp_order_id', 'order_date', 'order_time', 'branch_name', 
                 'product_name', 'product_size', 'unit_price', 'order_qty', 
                 'total_amount', 'payment_method']

    # convert list into diction with column names
    order_dict_list = convert_to_list_of_dictionary(transformed_data, key_names)

    # collapse the same transactions into one list
    unique_order_dict_list = collape_same_transactions_into_one(order_dict_list)
    

    for order_dict in unique_order_dict_list:
       
        order_date = order_dict['order_date']
        order_date = datetime.strptime(order_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        order_time = order_dict['order_time']
        branch_name = order_dict['branch_name']
        payment_method = order_dict['payment_method']
        total_order_amount = order_dict['total_amount']
        order_list = order_dict['orders']

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

        # query a newly-created order_id
        sql_order = """SELECT MAX(order_id)
                        FROM orders
                    """
        cursor.execute(sql_order)
        Order_id = cursor.fetchone()[0]

        for each_order_dict in order_list:
            
            product_name = each_order_dict['product_name']
            product_size = each_order_dict['product_size']
            order_qty = each_order_dict['order_qty']

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


            # Call the load_order_product_data to insert data into the order_product table
            load_order_product_data(order_product_data)

conn.commit()
cursor.close()
conn.close()