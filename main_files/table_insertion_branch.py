from main_files.databaseconn_main import *
from main_files.functions_main import *

def insert_branches(conn, cursor, branch_name: str):
    sql = '''SELECT COUNT(*)
             FROM branches 
             WHERE branch_name = %s
             '''
    data_values = (branch_name,)

    cursor.execute(sql, data_values)
    existing_branch = cursor.fetchone()[0]

    if existing_branch:
        print(f"Branch with name {branch_name} already exists in the database.")
    else:
        sql = '''INSERT INTO branches 
                 (branch_name)
                 VALUES (%s)
                 '''
        data_values = (branch_name,)

        cursor.execute(sql, data_values)
        conn.commit()
        print(f"New row with branch name {branch_name} was inserted.")

csv_files = get_csv_files_path() 

unique_branch_names = set()

for file_path in csv_files:
    csv_reader = read_csv(file_path)

    for row in csv_reader:
        branch_name = row[1]

        # Add the branch name to the set of unique branch names
        unique_branch_names.add(branch_name)

# Convert the set of unique branch names to a list
branch_names = list(unique_branch_names)

# Sort the list of branch names alphabetically
branch_names.sort()

conn, cursor = database_connection(dbname, user, password, host, port)

for branch_name in branch_names:
    insert_branches(conn, cursor, branch_name)

cursor.close()
conn.close()
