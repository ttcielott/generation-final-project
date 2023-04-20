import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('../database/.env')  # load environment variables from .env file

dbname = os.getenv("postgresql_db")
user = os.getenv("postgresql_user")
host = os.getenv("postgresql_host")
port = os.getenv("postgresql_port")
password = os.getenv("postgresql_pass")

# Connect to the database
def database_connection(dbname, user, password, host, port):
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    cursor = conn.cursor()
    return conn,cursor
