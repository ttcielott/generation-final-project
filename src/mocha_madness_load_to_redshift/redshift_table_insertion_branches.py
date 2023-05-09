from database.redshift_db_conn import *
from typing import List

def get_unique_branch_names(record_index, from_path, list_of_data_list: List):
    
    unique_branch_names = set()
    for row in list_of_data_list:

        branch_name = row[3]

        # Add the branch name to the set of unique branch names
        unique_branch_names.add(branch_name)

    # Convert the set of unique branch names to a list
    branch_names = list(unique_branch_names)

    # Sort the list of branch names alphabetically
    branch_names.sort()

    return branch_names


def insert_branch(record_index: int, from_path:str, conn, cursor, branch_name: str):
    try:

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
    except Exception as e:
        print(f"""lambda_handler record_index = {record_index}
                    from path {from_path},
                    the function, 'insert_branches' has issue. 
                    Error message: {e}""")


def load_to_table_branches(record_index, from_path, data):
    
    conn, cursor = database_connection(dbname, user, password, host, port)
    
    branch_names = get_unique_branch_names(record_index, from_path, data)

    for branch_name in branch_names:
        insert_branch(record_index, from_path, conn, cursor, branch_name)

    cursor.close()
    conn.close()
