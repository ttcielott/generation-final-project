import csv
from operator import itemgetter

def extract_without(file_path, column_numbers):
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

def split_size_as_column(list_of_data_list, column_number, sep=' '):
    list_of_new_data_list =[]
    for data in list_of_data_list:
        updating_col = data[column_number]
        striped_string = updating_col.strip()
        print(striped_string)
        split_list= striped_string.split(sep, 1)

        if len(split_list) == 1:
            raise Exception('No split occurred')
        elif len(split_list) > 1:
            
            original_data = data.copy()
            original_data[column_number] = split_list[0]
            original_data.append(split_list[1])
            list_of_new_data_list.append(original_data)

    return list_of_new_data_list

def split_unitprice_as_column(list_of_data_list, column_number, sep=' - '):
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
        
if __name__ == "__main__":
    new_data = extract_without('../data/chesterfield_25-08-2021_09-00-00.csv', [6])

    new_data = split_into_order(new_data, 3)

    new_data = split_size_as_column(new_data[3:10], 3)

    new_data = split_unitprice_as_column(new_data[3:10], 6)

    for ele in new_data:
        print(ele)