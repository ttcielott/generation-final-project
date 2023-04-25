# Import db connection previously created
from databaseconn_main import *

conn,cur = database_connection(dbname, user, password, host, port)

# Simply function to insert 2 different payment options in payments table
cur.execute("INSERT INTO payments (payment_method_id, payment_method_name) VALUES (%s, %s)", (1, 'CARD'))
cur.execute("INSERT INTO payments (payment_method_id, payment_method_name) VALUES (%s, %s)", (2, 'CASH'))
conn.commit()
print('Rows Added')
conn.close()