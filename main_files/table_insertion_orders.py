from main_files.databaseconn_main import *
from main_files.functions_main import *
from typing import List, Dict
from datetime import datetime


def insert_order(order_dict: Dict):
    conn, cursor = database_connection(dbname, user, password, host, port)

    branch_id = order_dict["branch_id"]
    payment_method_id = order_dict["payment_method_id"]
    total_order_amount = order_dict["total_order_amount"]
    order_date = order_dict["order_date"]
    order_time = order_dict["order_time"]

    cursor.execute(
        """
        INSERT INTO orders
        (branch_id, payment_method_id, total_order_amount, order_date, order_time)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (branch_id, payment_method_id, total_order_amount, order_date, order_time)
    )
    cursor.close()
    conn.commit()
    conn.close()
    
def insert_order_product(order_product_dict: Dict):
    conn, cursor = database_connection(dbname, user, password, host, port)
    
    order_id = order_product_dict["order_id"]
    product_id = order_product_dict["product_id"]
    order_qty = order_product_dict["order_qty"]

    cursor.execute(
        """
        INSERT INTO order_product
        (order_id, product_id, order_qty)
        VALUES (%s, %s, %s)
        """,
        (order_id, product_id, order_qty)
    )
    cursor.close()
    conn.commit()
    conn.close()

def get_unique_orders_dictionaries(record_index: int, from_path: str, list_of_data: List):

    # set key names
    key_names = ['temp_order_id', 'order_date', 'order_time', 'branch_name', 
                    'product_name', 'product_size', 'unit_price', 'order_qty', 
                    'total_amount', 'payment_method']

    # convert list into diction with column names
    order_dict_list = convert_to_list_of_dictionary(list_of_data, key_names)

    # collapse the same transactions into one list
    unique_order_dict_list = collape_same_transactions_into_one(order_dict_list)

    return unique_order_dict_list

def load_to_table_order_n_order_product(record_index: int, from_path: str, list_of_data: List):

    conn, cursor = database_connection(dbname, user, password, host, port)

    unique_order_dict_list = get_unique_orders_dictionaries(record_index, from_path, list_of_data)

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
                        WHERE branch_name = %s; 
                        """
        sql_payment = """SELECT payment_method_id
                            FROM payments
                            WHERE payment_method_name = %s;
                        """
        
        branch_values = (branch_name,)
        cursor.execute(sql_branch, branch_values)
        Branch_id = cursor.fetchone()[0]
        print(f'branch_id:{Branch_id}')

        payment_values = (payment_method,)
        cursor.execute(sql_payment, payment_values)
        Payment_method_id = cursor.fetchone()[0]
        print(f'payment_method_id: {Payment_method_id}')


        # save the information to be inserted into the table, order as a dictionary
        order_data = {"branch_id": Branch_id, 
                    "payment_method_id": Payment_method_id, 
                    "total_order_amount": total_order_amount, 
                    "order_date": order_date, "order_time": order_time}
        print(f'order_data: {order_data}')

        # insert data into the orders table
        insert_order(order_data)
        
        conn, cursor = database_connection(dbname, user, password, host, port)
        
        # query a newly-created order_id
        sql_order = """SELECT MAX(order_id)
                        FROM orders;
                    """
        cursor.execute(sql_order)
        Order_id = cursor.fetchone()[0]
        print(f'order_id: {Order_id}')

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
            
            # save the information to be inserted into the table, order_product as a dictionary
            order_product_data = {"order_id": Order_id,
                                    "product_id": Product_id, 
                                    "order_qty": order_qty}


            # insert data into the order_product table
            insert_order_product(order_product_data)
