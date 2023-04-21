import os
from dotenv import load_dotenv
from databaseconn_main import database_connection

load_dotenv('../database/.env')  # load environment variables from .env file

dbname = os.getenv("postgresql_db")
user = os.getenv("postgresql_user")
host = os.getenv("postgresql_host")
port = os.getenv("postgresql_port")
password = os.getenv("postgresql_pass")


conn,cursor = database_connection(dbname, user, password, host, port)


def create_db_tables(conn, cursor):
    
    create_products_table = \
    """
    CREATE TABLE IF NOT EXISTS products(
        product_id serial NOT NULL,
        product_name varchar(255) NOT NULL,
        product_size varchar(50) NOT NULL,
        product_price decimal(19,2) NOT NULL,
        PRIMARY KEY (product_id)
    );
    """
    create_branches_table = \
    """
        CREATE TABLE IF NOT EXISTS branches(
            branch_id serial NOT NULL,
            branch_name varchar(20) NOT NULL,
            PRIMARY KEY (branch_id)
        );
    """
    create_payments_table = \
    """
        CREATE TABLE IF NOT EXISTS payments(
            payment_method_id serial NOT NULL,
            payment_method_name varchar(10),
            PRIMARY KEY (payment_method_id)
        );
    """
    create_orders_table = \
    """
    CREATE TABLE IF NOT EXISTS orders(
        order_id serial NOT NULL,
        branch_id int NOT NULL,
        product_id int NOT NULL,
        payment_method_id int NOT NULL,
        total_order_amount decimal(19,2),
        order_date date,
        order_time time,
        PRIMARY KEY (order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
        FOREIGN KEY (payment_method_id) REFERENCES payments(payment_method_id)
    );
    """
    
    cursor.execute(create_products_table)
    cursor.execute(create_branches_table)
    cursor.execute(create_payments_table)
    cursor.execute(create_orders_table)
    conn.commit()
    cursor.close()
    conn.close()

create_db_tables(conn, cursor)