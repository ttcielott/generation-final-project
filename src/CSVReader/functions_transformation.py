import csv
from operator import itemgetter
from typing import List
from collections import Counter

def read_csv(file):
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
    """make one row contain a single menu order and count add the number of the orders as a separate data

    Args:
        list_of_data_list: list, list of list from source csv file
        column_number: int
        sep: separator, dafault is ','.
    
    Returns:
        a list of list of data that each list is about one menu order
        example:
            original data: [[1, '05/05/2012 09:00', 'Large Flavoured latte - Hazelnut - 2.85, Regular Flat white - 2.15', 13.0]]
            column_numbers: [1]

            output:
            [[1, '05/05/2012 09:00', 'Mochafield', 'Large Flavoured latte - Hazelnut - 2.85', 1, 13.0],
             [1, '05/05/2012 09:00', 'Mochafield', 'Regular Flat white - 2.15', 1, 13.0]]
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
            unit_price = float(split_list[1])
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

            transaction_date = split_list[0]
            transaction_time = split_list[1]
            original_data.insert(1, transaction_date)
            original_data.insert(2, transaction_time)
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

