from database.redshift_db_conn import conn, cursor
import json

def create_db_tables(conn, cursor):
    try:
        create_products_table = \
        """
        CREATE TABLE IF NOT EXISTS products(
            product_id int identity(1,1) NOT NULL,
            product_name varchar(255) NOT NULL,
            product_size varchar(50) NOT NULL,
            product_price decimal(19,2) NOT NULL,
            PRIMARY KEY (product_id)
        );
        """
        create_branches_table = \
        """
            CREATE TABLE IF NOT EXISTS branches(
                branch_id int identity(1,1) NOT NULL,
                branch_name varchar(20) NOT NULL,
                PRIMARY KEY (branch_id)
            );
        """
        create_payments_table = \
        """
            CREATE TABLE IF NOT EXISTS payments(
                payment_method_id int identity(1,1) NOT NULL,
                payment_method_name varchar(10),
                PRIMARY KEY (payment_method_id)
            );
        """
        create_transactions_table = \
        """
        CREATE TABLE IF NOT EXISTS transactions(
            transaction_id int identity(1,1) NOT NULL,
            transaction_date date,
            transaction_time time,
            branch_id int NOT NULL,
            payment_method_id int NOT NULL,
            total_transaction_amount decimal(19,2),
            PRIMARY KEY (transaction_id),
            FOREIGN KEY (branch_id) REFERENCES branches(branch_id),
            FOREIGN KEY (payment_method_id) REFERENCES payments(payment_method_id)
        );
        """
        create_orders_table = \
        """
            CREATE TABLE IF NOT EXISTS orders(
                transaction_id int NOT NULL,
                product_id int NOT NULL,
                order_qty int NOT NULL,
                PRIMARY KEY (transaction_id, product_id, order_qty),
                FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
               
            );
        """
        
        cursor.execute(create_products_table)
        print('create_products_table is completed')
        cursor.execute(create_branches_table)
        print('create_branches_table is completed')
        cursor.execute(create_payments_table)
        print('create_payments_table is completed')
        cursor.execute(create_transactions_table)
        print('create_transactions_table is completed')
        cursor.execute(create_orders_table)
        print('create_orders_table is completed')
        conn.commit()
        cursor.close()
        conn.close()
        print('database connection is closed.')
    except Exception as e:
        print('create_db_tables, error message: {e}')
        
def lambda_handler(event, context):
    
    print('lambda_handler started event collected is {event}')
    
    create_db_tables(conn, cursor)
    print('create_db_tables is completed.')
    
    return {
        'statusCode': 200,
        'body': json.dumps('mocha-madness-TableSchemaCreator completed!')
    }
        
