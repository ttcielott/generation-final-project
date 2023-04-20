import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
HOST = os.environ.get("postgresql_host")
USER = os.environ.get("postgresql_user")
PASSWORD = os.environ.get("postgresql_pass")
WAREHOUSE_DB_NAME = os.environ.get("postgresql_db")

def create_db_tables(connection, cursor):
    
    create_products_table = \
    """
    CREATE TABLE IF NOT EXISTS products(
        product_id int NOT NULL,
        product_name varchar(255) NOT NULL,
        product_size varchar(50) NOT NULL,
        product_price decimal(19,2) NOT NULL,
        PRIMARY KEY (product_id)
    );
    """
    create_branches_table = \
    """
        CREATE TABLE IF NOT EXISTS branches(
            branch_id int NOT NULL,
            branch_name varchar(20) NOT NULL,
            PRIMARY KEY (branch_id)
        );
    """
    create_customers_table = \
    """
    CREATE TABLE IF NOT EXISTS customers(
        customer_id int NOT NULL,
        customer_name varchar(255) NOT NULL,
        customer_credit_card varchar(16) NOT NULL,
        PRIMARY KEY (customer_id)
    );
    """
    create_payments_table = \
    """
        CREATE TABLE IF NOT EXISTS payments(
            payment_method_id int NOT NULL,
            payment_method_name varchar(10),
            PRIMARY KEY (payment_method_id)
        );
    """
    create_orders_table = \
    """
    CREATE TABLE IF NOT EXISTS orders(
        order_id SERIAL NOT NULL,
        branch_id int NOT NULL,
        customer_id int NOT NULL,
        product_id int NOT NULL,
        payment_method_id int NOT NULL,
        total_order_amount decimal(19,2),
        order_date date,
        order_time time,
        PRIMARY KEY (order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (payment_method_id) REFERENCES payments(payment_method_id)
    );
    """
    
    cursor.execute(create_products_table)
    cursor.execute(create_branches_table)
    cursor.execute(create_customers_table)
    cursor.execute(create_payments_table)
    cursor.execute(create_orders_table)
    connection.commit()
    cursor.close()
    connection.close()

