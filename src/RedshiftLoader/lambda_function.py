import boto3
import csv
from io import StringIO
from database.redshift_db_conn import *
from RedshiftLoader.redshift_table_insertion_products import *
from RedshiftLoader.redshift_table_insertion_branches import *
from RedshiftLoader.redshift_table_insertion_payments import *
from RedshiftLoader.redshift_table_insertion_transactions_n_orders import *

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    print(f'lambda_handler started event collected is {event}')
    
    try:
        for msg_no, msg in enumerate(event['Records']):
            print(f'lambda_handler: msg_no = {msg_no}')
            message_body = msg['body']
            msg_body_json = json.loads(message_body)
            print(f'lambda_handler: msg_body_json loaded okay')
            bucket = msg_body_json['bucket']
            key = msg_body_json['key']
            print(f'lambda_handler: bucket = {bucket} and key = {key}')
                    
            from_path = f's3://{bucket}/{key}'
            print(f'lambda_handler msg_no= {msg_no} from path {from_path}')
            
            
            # access the conent of new data
            response = s3.get_object(Bucket=bucket, Key=key)
            content = response['Body'].read().decode('utf-8')

            # read the csv file of new data
            data = []
            reader = csv.reader(StringIO(content))
            for row in reader:
                    data.append(row)
            print(f'lambda_handler loaded {len(data)} rows from file {from_path}')
            
            # table, products
            load_to_table_products(msg_no, from_path, data)
            print(f'lambda_handler from path {from_path}, the function, load_to_table_products is completed')


            # table, branches
            load_to_table_branches(msg_no, from_path, data)
            print(f'lambda_handler from path {from_path}, the function, load_to_table_branches is completed')

            # table, payments
            load_to_table_payments(msg_no, from_path, data)
            print(f'lambda_handler from path {from_path}, the function, load_to_table_payments is completed')

            # table, transactions & table, orders
            load_to_table_transactions_n_orders(msg_no, from_path, data)
            print(f'lambda_handler from path {from_path}, the function, load_to_table_transactions_n_orders is completed')
            
            print(f'lambda_handler finished for from_path = {from_path}')
    except Exception as e:
        print(f'Error in lambda_handler = {e}')