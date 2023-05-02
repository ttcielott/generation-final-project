import os
import csv
from operator import itemgetter
from typing import List, Dict
from collections import Counter

def extract_without(file_path: str, column_numbers: List):
    """extract all data but the column numbers in the list
    Args:
        file_path: str, csv file path
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

    with open(file_path) as file:
        reader = csv.reader(file, delimiter = ',')


        for row in reader:
            selected_column_numbers = set(range(len(row))) - set(column_numbers)
            
            new_data_list= itemgetter(*selected_column_numbers)(row)
            new_data_list = list(new_data_list)
            list_of_new_data_list.append(new_data_list)

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
            original_data[column_number] = split_list[0]
            original_data.append(split_list[1])
            list_of_new_data_list.append(original_data)

    return list_of_new_data_list

def split_into_order(list_of_data_list, column_number, sep=','):
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
        # remove white space
        white_space_removal = lambda x: x.strip()
        orders_list = [*map(white_space_removal, orders_list)]
        
        count_dict = Counter(orders_list)
        print(count_dict)

        for product, qty in count_dict.items():
            original_data = data.copy()
            original_data[column_number] = product
            original_data.append(qty)
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
            raise Exception('No split occurred')
        elif len(split_list) > 1:
            
            original_data = data.copy()
            original_data[column_number] = split_list[0]
            original_data.append(split_list[1])
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
            raise Exception('No split occurred')
        elif len(split_list) > 1:
            
            original_data = data.copy()
            original_data[column_number] = split_list[0]
            original_data.append(split_list[1])
            list_of_new_data_list.append(original_data)

    return list_of_new_data_list


def transform_branch_file(file_path: str):
    """apply all data transfromation function to raw csv file.

    Args:
        file_path: str, a signle branch's csv file path

    Returns:
        a list of list of data that contains transformed sale data of a single branch
    """

    # extract raw csv file without the column, customer name and credit card number
    transformed_data1 = extract_without(file_path, [2, 6])

    # split the column, datetime into date and time
    transformed_data2 = split_ordertime_as_column(transformed_data1, 0)

    # transform transformed_data2 to split multiple orders in one row into single order in one row
    transformed_data3 = split_into_order(transformed_data2, 2)

    # transform transformed_data3 to split size from order
    transformed_data4 = split_size_as_column(transformed_data3, 2)

    # transform transformed_data4 to split unit price from order
    transformed_data5 = split_unitprice_as_column(transformed_data4, -1)

    
    return transformed_data5

def get_csv_files_path():
    # Navigate to the data folder
    data_folder = "csv_files"
    
    # Get a list of all CSV files in the data folder
    csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]
    return csv_files



if __name__ == "__main__":
    branch_filepaths = get_csv_files_path()
    # apply all transformation functions in order and combine them into one list
    transformed_branch_data =[]
    for filepath in branch_filepaths:
        transformed_branch_data += transform_branch_file(filepath)

    print(len(transformed_branch_data))
    
    for ele in transformed_branch_data[:5]:
        print(ele)

    csv_files = get_csv_files_path()
    print(csv_files)