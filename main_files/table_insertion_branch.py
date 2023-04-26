import csv
import os
from main_files.databaseconn_main import *

def insert_branches(conn, cursor, branch_id, branch_name):
    cursor.execute("INSERT INTO branches (branch_id, branch_name) VALUES (%s, %s)", (branch_id, branch_name))
    conn.commit()
    print(f"New row with branch ID {branch_id} and branch name {branch_name} was inserted.")


# Get the path of the current file
current_file_path = os.path.dirname(__file__)

# Navigate to the data folder
data_folder = "csv_files"

# Get a list of all CSV files in the data folder
csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".csv")]

unique_branch_names = set()

for csv_file in csv_files:
    with open(csv_file, "r") as f:
        csv_reader = csv.reader(f)

        for row in csv_reader:
            branch_name = row[1]

            # Add the branch name to the set of unique branch names
            unique_branch_names.add(branch_name)

# Convert the set of unique branch names to a list
branch_names = list(unique_branch_names)

# Sort the list of branch names alphabetically
branch_names.sort()

new_rows = [(i+1, branch_names[i]) for i in range(len(branch_names))]

conn, cursor = database_connection(dbname, user, password, host, port)

for row in new_rows:
    insert_branches(conn, cursor, row[0], row[1])

cursor.close()
conn.close()
