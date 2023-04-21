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

conn, cursor = database_connection(dbname, user, password, host, port)

# save raw csv file path as a list
branch_filepaths = ['../data/chesterfield_25-08-2021_09-00-00.csv', '../data/leeds_01-01-2020_09-00-00.csv']
    
# apply all transformation functions in order and combine them into one list
transformed_branch_data =[]
for filepath in branch_filepaths:
    transformed_branch_data += transform_branch_file(filepath)


def get_unique_product_n_price(list_of_data_list):
      product_rows =[]
      for row in list_of_data_list:
            
            product_row = [row[-3], row[3], row[-2]]
            product_rows.append(product_row)
      
      # remove duplicates
      unique_product_row = set(map(tuple, product_rows))
      unique_product_info = list(map(list, unique_product_row))

      return unique_product_info


def load_product(conn, cursor, product_info, tablename):
      
      sql = f"""
            INSERT INTO {tablename}(product_name, product_size, product_price)
            VALUES (%s, %s, %s);
            """
      
      for row in product_info:
            
            data_values = tuple(row)
            cursor.execute(sql, data_values)
      conn.commit()
      cursor.close()
      conn.close()

if __name__ == '__main__':
      product_info = get_unique_product_n_price(transformed_branch_data)
      print(product_info)
      load_product(conn, cursor, product_info, 'products')


