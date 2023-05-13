from database.redshift_db_conn import *
from RedshiftLoader.functions_orders import get_unique_orders_dictinaries
from typing import List
from datetime import datetime


def load_to_table_transactions_n_orders(record_index: int, from_path: str, list_of_data: List):

    conn, cursor = database_connection(dbname, user, password, host, port)

    unique_order_dict_list = get_unique_orders_dictinaries(record_index, from_path, list_of_data)

    for order_dict in unique_order_dict_list:

        transaction_date = order_dict['transaction_date']
        transaction_date = datetime.strptime(transaction_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        transaction_time = order_dict['transaction_time']
        branch_name = order_dict['branch_name']
        payment_method = order_dict['payment_method']
        total_transaction_amount = order_dict['total_amount']
        orders_list = order_dict['orders_list']


        # fetch the branch_id of this transaction
        sql_branch = """SELECT branch_id
                        FROM branches
                        WHERE branch_name = %s 
                        """
        
        branch_values = (branch_name,)
        cursor.execute(sql_branch, branch_values)
        fetched_branch_id = cursor.fetchone()[0]

        # fetch the payment_method_id of this transaction
        sql_payment = """SELECT payment_method_id
                            FROM payments
                            WHERE payment_method_name = %s
                        """
        payment_values = (payment_method,)
        cursor.execute(sql_payment, payment_values)
        fetched_payment_method_id = cursor.fetchone()[0]


        # insert this transaction into the table, transactions
        cursor.execute(
            """
            BEGIN;
            INSERT INTO transactions
            (transaction_date, transaction_time, branch_id, payment_method_id, total_transaction_amount)
            VALUES (%s, %s, %s, %s, %s);
            COMMIT;
            SELECT transaction_id FROM transactions ORDER BY transaction_id DESC LIMIT 1; 
            """,
            (transaction_date, transaction_time, fetched_branch_id, fetched_payment_method_id, total_transaction_amount)
        )
        transaction_id = cursor.fetchone()

        # loop through one or more orders under this transaction
        for each_order_dict in orders_list:
            
            # save the combination of data values of this order
            product_name = each_order_dict['product_name']
            product_size = each_order_dict['product_size']
            order_qty = each_order_dict['order_qty']

            # fetch the product_id of this order
            sql_product = """SELECT product_id
                            FROM products
                            WHERE product_name = %s
                            AND product_size = %s 
                        """

            product_values = (product_name, product_size)
            cursor.execute(sql_product, product_values)
            fetched_product_id = cursor.fetchone()[0]

            # insert the information about this order into the table, orders
            cursor.execute(
            """
            INSERT INTO orders
            (transaction_id, product_id, order_qty)
            VALUES (%s, %s, %s)
            """,
            (transaction_id, fetched_product_id, order_qty)
            )


    conn.commit()
    cursor.close()
    conn.close()