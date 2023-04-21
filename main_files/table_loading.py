import os
from dotenv import load_dotenv
from databaseconn_main import database_connection
from functions_main import transform_branch_file

load_dotenv('../database/.env')  # load environment variables from .env file

dbname = os.getenv("postgresql_db")
user = os.getenv("postgresql_user")
host = os.getenv("postgresql_host")
port = os.getenv("postgresql_port")
password = os.getenv("postgresql_pass")

# create database connection and cursor
conn, cursor = database_connection(dbname, user, password, host, port)

# save raw csv file path as a list
branch_filepaths = ['../data/chesterfield_25-08-2021_09-00-00.csv', '../data/leeds_01-01-2020_09-00-00.csv']
    
# apply all transformation functions in order and combine them into one list
transformed_branch_data =[]
for filepath in branch_filepaths:
    transformed_branch_data += transform_branch_file(filepath)

# print transformed_branch_data
for ele in transformed_branch_data[:5]:
        print(ele)

# view the unique values of product names
product_names = set([row[-3] for row in transformed_branch_data])
print(product_names, len(product_names))


def load_data(conn, cursor, list_of_data_list, tablename, column_list, values_list):
      # join list element as str : e.g. ['product_id, 'product_name'] -> 'product_id, product_name'
      column_list_as_str = ','.join(column_list) 
      # create '%s' as many as number of columns: e.g. '%s, %s' when the numbe of columns is 2
      place_holder = ','.join(['%s'] * len(column_list)) # ['%s'] -> ['%s', '%s'] -> '%s, %s'

      sql = '''
            INSERT INTO {tablename}({column_list_as_str})
            VALUES ({place_holder})
            '''
      data_values = set(values_list)
      cursor.execute(sql, data_values)
      conn.commit()