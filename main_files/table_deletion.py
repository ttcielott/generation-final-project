import os
from dotenv import load_dotenv
from main_files.databaseconn_main import database_connection

load_dotenv('database/.env')  # load environment variables from .env file

dbname = os.getenv("postgresql_db")
user = os.getenv("postgresql_user")
host = os.getenv("postgresql_host")
port = os.getenv("postgresql_port")
password = os.getenv("postgresql_pass")


conn,cursor = database_connection(dbname, user, password, host, port)

def delete_db_tables(conn, cursor, table_names):

    delete_table= \
    f"""
    DROP TABLE IF EXISTS {table_names};
    """
    
    cursor.execute(delete_table)
    conn.commit()
    cursor.close()
    conn.close()

table_names = 'order_product, orders, payments, branches, products'
delete_db_tables(conn, cursor, table_names)