import os
from operator import itemgetter
from typing import List
from collections import Counter

def read_csv(file_path):
    with open(file_path) as file:
        csv_file = csv.reader(file, delimiter=',')
    
        csv_list = [*csv_file]
    return csv_list

def extract_without(list_of_data: List, column_numbers: List):
    """extract all data but the column numbers in the list
    Args:
        list_of_data: output from csv.reader()
        column_number: list of of column numbers to exclude
    
    Returns:
        a list of list of data without values in the columns that you set to exclude
        example:
            original data: [['a', 'b', 'c', 'd']], ['e', 'f', 'g', 'h']]
            column_numbers: [3]

            output:
            [['a', 'b', 'c], ['e', 'f', 'g']]
    """

    list_of_new_data_list = []

    for data in list_of_data:
        selected_column_numbers = set(range(len(data))) - set(column_numbers)
        selected_column_numbers = list(selected_column_numbers)
        
        new_data_list= itemgetter(*selected_column_numbers)(data)
        new_data_list = list(new_data_list)
        list_of_new_data_list.append(new_data_list)

    return list_of_new_data_list

def add_temp_transaction_id(list_of_data_list):

    list_of_new_data_list = []
    for i, data in enumerate(list_of_data_list):
        transaction_id = i + 1
        original_data = data.copy()
        original_data.insert(0, transaction_id)
        list_of_new_data_list.append(original_data)

    return list_of_new_data_list
        

def split_into_order(list_of_data_list, column_number, sep = ','):
    """make one row contain a single menu order. 

    Args:
        list_of_data_list: list, list of list from source csv file
        column_number: int
        sep: separator, dafault is ','.
    
    Returns:
        a list of list of data that each list is about one menu order
        example:
            original data: [['tom', 'Large Flavoured latte - Hazelnut - 2.85, Regular Flat white - 2.15', 13.0]]
            column_numbers: [1]

            output:
            [['tom','Large Flavoured latte - Hazelnut - 2.85', 13.0],
             ['tom','Regular Flat white - 2.15', 13.0]]
    """
    list_of_new_data_list =[]
    for data in list_of_data_list:
        updating_col = data[column_number]
        orders_list = updating_col.split(sep)
        
        white_space_removal = lambda x: x.strip()
        orders_list = [*map(white_space_removal, orders_list)]
        
        count_dict = Counter(orders_list)

        for product_name, order_qty in count_dict.items():
            original_data = data.copy()
            original_data.pop(column_number)

            original_data.insert(3, product_name)
            original_data.insert(4, order_qty)

            list_of_new_data_list.append(original_data)
                

    return list_of_new_data_list

def split_size_as_column(list_of_data_list: List, column_number: int, sep: str =' '):
    """split size from order into a separate column or element

    Args:
        list_of_data_list: list, ooutput of the function, `split_into_order`
        column_number: int
        sep: separator, dafault is ' '.

    Returns:
        a list of list of data with order size element is separated from order element and added as a separate element
        example:
            original data: [['tom','Large Flavoured latte - Hazelnut - 2.85', 13.0],
                            ['tom','Regular Flat white - 2.15', 13.0]]
            column_numbers: [1]

            output:
            [['tom','Flavoured latte - Hazelnut - 2.85', 13.0, 'Large'],
             ['tom','Flat white - 2.45', 13.0, 'Regular']]
    """
    list_of_new_data_list =[]
    for data in list_of_data_list:
        updating_col = data[column_number]
        striped_string = updating_col.strip()
        split_list= striped_string.split(sep, 1)

        if len(split_list) == 1:
            raise Exception('No split occurred in size column')
        elif len(split_list) > 1:
            
            original_data = data.copy()
            original_data.pop(column_number)

            product_size = split_list[0]
            product_name = split_list[1]
            original_data.insert(3, product_name)
            original_data.insert(4, product_size)
            
            list_of_new_data_list.append(original_data)

    return list_of_new_data_list

def split_unitprice_as_column(list_of_data_list: List, column_number: int, sep: str =' - '):
    """split unit prince from order into a separate column or element

    Args:
        list_of_data_list: list, output of the function, `split_size_as_column`
        column_number: int
        sep: separator, dafault is ' - '.

    Returns:
        a list of list of data with unit price element separated from order element and added as a separate element
        example:
            original data:   [['tom','Flavoured latte - Hazelnut - 2.85', 13.0, 'Large'],
                              ['tom','Flat white - 2.45', 13.0, 'Regular']]
            column_numbers: [1]

            output:
             [['tom','Flavoured latte - Hazelnut', 13.0, 'Large', 2.85],
              ['tom','Flat white', 13.0, 'Regular', 2.45]]
    """
    list_of_new_data_list =[]
    for data in list_of_data_list:
        updating_col = data[column_number]
        split_list = updating_col.strip().rsplit(sep, 1)

        if len(split_list) == 1:
            raise Exception('No split occurred in unit price column')
        elif len(split_list) > 1:
            
            original_data = data.copy()
            original_data.pop(column_number)

            product_name = split_list[0]
            unit_price = split_list[1]
            original_data.insert(3, product_name)
            original_data.insert(5, unit_price)

            list_of_new_data_list.append(original_data)

    return list_of_new_data_list


def split_ordertime_as_column(list_of_data_list: List, column_number: int, sep: str=' '):
    """split order time from order date time into a separate column or element

    Args:
        list_of_data_list: list, output of the function, `split_unitprice_as_column`
        column_number: int
        sep: separator, dafault is ' '.

    Returns:
        a list of list of data with order time element separated from order date time element and added as a separate element
        example:
            original data:   [['25/08/2021 09:00','Chesterfield', 'Richard']]
            column_numbers: [0]

            output:
            [['25/08/2021','Chesterfield', 'Richard', '09:00']]
    """
    list_of_new_data_list =[]
    for data in list_of_data_list:
        updating_col = data[column_number]
        split_list = updating_col.strip().split(sep, 1)

        if len(split_list) == 1:
            raise Exception('No split occurred')
        elif len(split_list) > 1:
            
            original_data = data.copy()
            original_data.pop(column_number)

            order_date = split_list[0]
            order_time = split_list[1]
            original_data.insert(1, order_date)
            original_data.insert(2, order_time)
            list_of_new_data_list.append(original_data)

    return list_of_new_data_list

def transform_branch_file(list_of_data: List):
    """apply all data transfromation function to raw csv file.

    Args:
        file_path: str, a signle branch's csv file path

    Returns:
        a list of list of data that contains transformed sale data of a single branch
    """

    new_data = extract_without(list_of_data, [2, 6])

    new_data = add_temp_transaction_id(new_data)

    new_data = split_into_order(new_data, 3)

    new_data = split_size_as_column(new_data, 3)

    new_data = split_unitprice_as_column(new_data, 3)

    new_data = split_ordertime_as_column(new_data, 1)

    
    return new_data

def convert_to_list_of_dictionary(list_of_data: List, key_names: List):
    # make a list of dictionaries of which the key, 'order_list' contain a list of all orders per each transaction
    # each order in order_list should be in the dictionary: {'product_name': 'latte', 'product_size': 'large', 'order_qty': 2}
    order_dict_list = []
    for order_list in list_of_data:
        order_dict = dict(zip(key_names, order_list))
        order_dict_list.append(order_dict)
    
    return order_dict_list

def collape_same_transactions_into_one(order_dict_list: List):
    new_order_dict_list = []
    for order_dict in order_dict_list:
        single_order_dict = {'product_name': order_dict['product_name'], 
                              'product_size': order_dict['product_size'],
                              'order_qty': order_dict['order_qty']}
        if len(new_order_dict_list) > 0 and order_dict['temp_order_id'] == new_order_dict_list[-1]['temp_order_id']:
            # last_added_order_dict = new_order_dict_list[-1]
            # last_added_order_id_key = last_added_order_dict['temp_order_id']
            # current_order_id_key = order_dict['temp_order_id']
            
            new_order_dict_list[-1]['orders'].append(single_order_dict)
        else:
            order_dict['orders'] = [single_order_dict]
            del order_dict['product_name']
            del order_dict['product_size']
            del order_dict['order_qty']
            new_order_dict_list.append(order_dict)

    return new_order_dict_list

def get_csv_files_path():
    # Navigate to the data folder
    data_folder = "csv_files"
    
    # Get a list of all CSV files in the data folder
    csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]
    return csv_files



    

import csv

if __name__ == "__main__":
    csv_path = 'csv_files/chesterfield_25-08-2021_09-00-00.csv'

    csv_list = read_csv(csv_path)

    transform_data = transform_branch_file(csv_list)

    for row in transform_data[:10]:
        print(row)

    key_names = ['temp_order_id', 'order_date', 'order_time', 'branch_name', 
                 'product_name', 'product_size', 'unit_price', 'order_qty', 
                 'total_amount', 'payment_method']
    
    order_dict_list = convert_to_list_of_dictionary(transform_data[:10], key_names=key_names)

    collapsed_dict_list = collape_same_transactions_into_one(order_dict_list)

    for row in collapsed_dict_list:
        for key, value in row.items():
            print(f'{key} : {value} \n')
