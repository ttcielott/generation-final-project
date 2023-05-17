from database.redshift_db_conn import *
from typing import List

def get_unique_payment_methods(record_index: int, from_path: str, list_of_data: List):

    unique_payment_names = set()
    for row in list_of_data:
        payment_method_name = row[-1]

        # Add the payment name to the set of unique payment names
        unique_payment_names.add(payment_method_name)

    # Convert the set of unique branch names to a list
    payment_method_names = list(unique_payment_names)

    # Sort the list of branch names alphabetically
    payment_method_names.sort()

    return unique_payment_names


# Simply function to insert payment options in payments table
def insert_payment(conn, cursor, payment_method_name: str):
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




def load_to_table_payments(record_index, from_path, data):

    conn, cursor = database_connection(dbname, user, password, host, port)
    
    payment_method_names = get_unique_payment_methods(record_index, from_path, data)

    for payment_method_name in payment_method_names:
        insert_payment(conn, cursor, payment_method_name)

    cursor.close()
    conn.close()