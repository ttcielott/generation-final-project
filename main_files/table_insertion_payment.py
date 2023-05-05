# Import db connection previously created
import csv
import os
from main_files.databaseconn_main import *
from main_files.functions_main import *

# Simply function to insert payment options in payments table

def insert_payment (conn, cursor, payment_method_id:int, payment_method_name:str):
    '''
    This function reads files in the data folder and then returns 
    the unique payment methods stored in each csv file, if a different
    method is found then it will add it to the db table 
    '''
    cursor.execute("INSERT INTO payments (payment_method_id, payment_method_name) VALUES (%s, %s)", (payment_method_id, payment_method_name))
    conn.commit()
    print('Rows Added')

csv_files = get_csv_files_path() 

unique_payment_names = set()

for csv_file in csv_files:
    with open(csv_file, "r") as f:
        csv_reader = csv.reader(f)

        for row in csv_reader:
            payment_method_name = row[5]

            # Add the payment name to the set of unique payment names
            unique_payment_names.add(payment_method_name)

# Convert the set of unique branch names to a list
payment_method_names = list(unique_payment_names)

# Sort the list of branch names alphabetically
payment_method_names.sort()

new_rows = [(i+1, payment_method_names[i]) for i in range(len(payment_method_names))]

conn, cursor = database_connection(dbname, user, password, host, port)

for row in new_rows:
    insert_payment(conn, cursor, row[0], row[1])

cursor.close()
conn.close()