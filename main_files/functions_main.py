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


        
if __name__ == "__main__":
    print(extract_without('../data/chesterfield_25-08-2021_09-00-00.csv', [6]))