# Import db connection previously created
import csv
from main_files.databaseconn_main import *
from main_files.functions_main import *

# Simply function to insert payment options in payments table

def insert_payment (conn, cursor, payment_method_name: str):
    '''
    This function reads files in the data folder and then returns 
    the unique payment methods stored in each csv file, if a different
    method is found then it will add it to the db table 
    '''
    
    sql = '''SELECT COUNT(*)
             FROM payments
             WHERE payment_method_name = %s
             '''
    data_values = (payment_method_name,)

    cursor.execute(sql, data_values)
    existing_payment_method = cursor.fetchone()[0]

    if existing_payment_method :
        print(f"The payment method, {payment_method_name} already exists in the database.")

    else:
        sql = '''INSERT INTO payments 
                (payment_method_name)
                VALUES (%s)
                '''
        data_values = (payment_method_name,)
        cursor.execute(sql, data_values)
        conn.commit()
        print(f'New row with {payment_method_name} was inserted.')

csv_files = get_csv_files_path() 

unique_payment_names = set()

for file_path in csv_files:
    csv_reader = read_csv(file_path)

    for row in csv_reader:
        payment_method_name = row[5]

        # Add the payment name to the set of unique payment names
        unique_payment_names.add(payment_method_name)

# Convert the set of unique branch names to a list
payment_method_names = list(unique_payment_names)

# Sort the list of branch names alphabetically
payment_method_names.sort()

conn, cursor = database_connection(dbname, user, password, host, port)

for payment_method_name in payment_method_names:
    insert_payment(conn, cursor, payment_method_name)

cursor.close()
conn.close()