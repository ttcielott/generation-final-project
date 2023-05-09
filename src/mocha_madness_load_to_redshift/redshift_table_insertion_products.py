from database.redshift_db_conn import *
from typing import List

def get_unique_product_info_combination(record_index: int, from_path: str, list_of_data_list: List):
    """get the list of unique product infomation lists.

    Args:
        list_of_data_list: a list of list that contains transformed data

    Returns:
        a list of product infomrmation 
        e.g. [[['Chai latte', 'Large', '2.60'], 
               ['Chai latte', 'Regular', '2.30'], 
               ['Filter coffee', 'Large', '1.80']]
    """
    try:
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

    except Exception as e:
        print(f'''lambda_handler record_index = {record_index} \
                    from path {from_path}, \
                    the function, 'get_unique_product_n_price' has issue. \
                    Error message: {e}''')

    return unique_product_info


def insert_product(record_index, from_path, conn, cursor, product_info):
    try:
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
                print(f'''lambda_handler record_index = {record_index} from path {from_path}, 
                    The product information,
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
        
                print(f'''lambda_handler record_index = {record_index} from path {from_path}, 
                    New row with the product information,
                    [product_name: {product_info[0]}, 
                    product_size: {product_info[1]}, 
                    product_price: {product_info[2]}] was inserted.''')
                
    except Exception as e:
        print(f'''lambda_handler record_index = {record_index}
                    from path {from_path},
                    the funciton, 'load_product' has issue. 
                    Error message: {e}''')


def load_to_table_products(record_index, from_path, data):
    
    conn, cursor = database_connection(dbname, user, password, host, port)
    
    product_info_list = get_unique_product_info_combination(record_index, from_path, data)

    for product_info in product_info_list:
        insert_product(record_index, from_path, conn, cursor, product_info)

    cursor.close()
    conn.close()