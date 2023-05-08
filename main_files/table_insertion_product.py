from main_files.databaseconn_main import *
from main_files.functions_main import transform_branch_file
from typing import List
from main_files.functions_main import *



csv_files = get_csv_files_path()

# apply all transformation functions in order and combine them into one list
transformed_branch_data =[]
for filepath in csv_files:
      csv_list = read_csv(filepath)
      transformed_branch_data += transform_branch_file(csv_list)


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
            product_row = [row[4], row[5], row[6]]

            # append product_row to product_rows
            product_rows.append(product_row)
      
      # remove duplicates
      unique_product_row = set(map(tuple, product_rows)) # e.g. {('Filter coffee', 'Large', '1.80'), ('Filter coffee', 'Large', '1.80')}
      unique_product_info = list(map(list, unique_product_row)) # e.g. [['Filter coffee', 'Large', '1.80'], ['Filter coffee', 'Large', '1.80']]

      # sort the data
      unique_product_info.sort()

      return unique_product_info


def load_product(conn, cursor, product_info):
      sql = '''SELECT COUNT(*)
             FROM products
             WHERE product_name = %s
             AND product_size = %s
             AND product_price = %s;
             '''
      
      data_values = tuple(product_info)
      cursor.execute(sql, data_values)
      existing_product_info = cursor.fetchone()[0]

      if existing_product_info :
            print(f'''The product information,
                  [product_name: {product_info[0]}, 
                  product_size: {product_info[1]}, 
                  product_price: {product_info[2]}] already exists in the database.''')

      else:
            sql = f"""
                  INSERT INTO products(product_name, product_size, product_price)
                  VALUES (%s, %s, %s);
                  """
            cursor.execute(sql, data_values)
            conn.commit()
      
            print(f'''New row with the product information,
                  [product_name: {product_info[0]}, 
                  product_size: {product_info[1]}, 
                  product_price: {product_info[2]}] was inserted.''')


if __name__ == '__main__':
      product_info_list = get_unique_product_n_price(transformed_branch_data)

      # create a database connnection
      conn, cursor = database_connection(dbname, user, password, host, port)

      for product_info in product_info_list:
            load_product(conn, cursor, product_info)

      cursor.close()
      conn.close()

