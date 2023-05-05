import os
import csv
from operator import itemgetter
from typing import List, Dict

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
            selected_column_numbers = list(selected_column_numbers)
            
            new_data_list= itemgetter(*selected_column_numbers)(row)
            new_data_list = list(new_data_list)
            list_of_new_data_list.append(new_data_list)

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

        if len(orders_list) == 1:
            list_of_new_data_list.append(data)
        elif len(orders_list) > 1:
            for single_order in orders_list:
                original_data = data.copy()
                original_data[column_number] = single_order
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

def transform_branch_file(file_path: str):
    """apply all data transfromation function to raw csv file.

    Args:
        file_path: str, a signle branch's csv file path

    Returns:
        a list of list of data that contains transformed sale data of a single branch
    """

    new_data = extract_without(file_path, [6])

    new_data = split_into_order(new_data, 3)

    new_data = split_size_as_column(new_data, 3)

    new_data = split_unitprice_as_column(new_data, 6)

    new_data = split_ordertime_as_column(new_data, 0)
    
    return new_data

def get_csv_files_path():
    # Navigate to the data folder
    data_folder = "csv_files"
    
    # Get a list of all CSV files in the data folder
    csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]
    return csv_files

if __name__ == "__main__":
    branch_filepaths = ['csv_files/chesterfield_25-08-2021_09-00-00.csv', 'csv_files/leeds_01-01-2020_09-00-00.csv']
    # apply all transformation functions in order and combine them into one list
    transformed_branch_data =[]
    for filepath in branch_filepaths:
        transformed_branch_data += transform_branch_file(filepath)
    
    for ele in transformed_branch_data:
        print(ele)

    csv_files = get_csv_files_path()
    print(csv_files)