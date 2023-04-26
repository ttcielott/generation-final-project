import os
from dotenv import load_dotenv
from main_files.databaseconn_main import *
from main_files.functions_main import transform_branch_file
from typing import List


# create a database connnection
conn, cursor = database_connection(dbname, user, password, host, port)

# Get the path of the current file
current_file_path = os.path.dirname(__file__)

# Navigate to the data folder
data_folder = "csv_files"

# Get a list of all CSV files in the data folder
csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]
    
# apply all transformation functions in order and combine them into one list
transformed_branch_data =[]
for filepath in csv_files:
    transformed_branch_data += transform_branch_file(filepath)


def get_unique_product_n_price(list_of_data_list: List):
      """get the list of unique product infomation lists.

    Args:
        list_of_data_list: a list of list that contains transformed data

    Returns:
        a list of product infomrmation 
        e.g. [[['Chai latte', 'Large', '2.60'], 
               ['Chai latte', 'Regular', '2.30'], 
               ['Filter coffee', 'Large', '1.80']]
    """
      product_rows =[]
      # loop over all product information in transformed data
      for row in list_of_data_list:

            # select product name, product size, product price
            # save them in a list
            product_row = [row[-3], row[3], row[-2]]

            # append product_row to product_rows
            product_rows.append(product_row)
      
      # remove duplicates
      unique_product_row = set(map(tuple, product_rows)) # e.g. {('Filter coffee', 'Large', '1.80'), ('Filter coffee', 'Large', '1.80')}
      unique_product_info = list(map(list, unique_product_row)) # e.g. [['Filter coffee', 'Large', '1.80'], ['Filter coffee', 'Large', '1.80']]

      # sort the data
      unique_product_info.sort()

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
      load_product(conn, cursor, product_info, 'products')


