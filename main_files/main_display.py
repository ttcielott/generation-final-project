import os
import csv
import pandas as pd
import psycopg2
import pyfiglet
from functions_main import *
from dotenv import load_dotenv
from unittesting_main import *
from databaseconn_main import *

load_dotenv()  # load environment variables from .env file

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