import csv
from functions_main import transform_branch_file

# filenames = ['./chesterfield_25-08-2021_09-00-00.csv', './leeds_01-01-2020_09-00-00.csv']

# for filename in filenames:
#     with open(filename, 'r') as file:
#         csv_data = csv.reader(file)
#         row_id = 1
#         for row in csv_data:
#             payment_method = row[5]
#             card_number = row[6]
#             print(row_id, payment_method, card_number)
#             row_id += 1