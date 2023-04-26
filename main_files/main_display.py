import os
import csv
import pandas as pd
import psycopg2
import pyfiglet
from main_files.functions_main import *
from dotenv import load_dotenv
from main_files.table_creation import *
from main_files.unittesting_main import *
from main_files.databaseconn_main import *

load_dotenv('database/.env')  # load environment variables from .env file

while True:
    # Connect to the database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    if conn:
        ascii_banner = pyfiglet.figlet_format(""" Mocha Madness!!""")
        print(ascii_banner)

    break