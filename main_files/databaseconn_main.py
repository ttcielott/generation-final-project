import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

dbname = os.getenv("postgresql_db")
user = os.getenv("postgresql_user")
host = os.getenv("postgresql_host")
port = os.getenv("postgresql_port")
password = os.getenv("postgresql_pass")

# Connect to the database
conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

cursor = conn.cursor()
