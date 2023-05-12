import boto3
import csv
from io import StringIO
from database.redshift_db_conn import *
from redshift_table_insertion_products import *
from redshift_table_insertion_branches import *
from redshift_table_insertion_payments import *
from redshift_table_insertion_orders import *

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    print(f'lambda_handler started event collected is {event}')
    
    for record_index, record in enumerate(event['Records']):
        print(f'lambda_handler is processing the record_index = {record_index}')
        
        # get new data's bucket and key information
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        from_path = f's3://{bucket}/{key}'
        print(f'lambda_handler record_index= {record_index} from path {from_path}')
        
        
        # access the conent of new data
        response = s3.get_object(Bucket=bucket, Key=key)
        print(f'lambda_handler s3 response = {response}')
        content = response['Body'].read().decode('utf-8')
        print(f'lambda_handler s3 content = {content}')
    
        # read the csv file of new data
        data = []
        reader = csv.reader(StringIO(content))
        for row in reader:
            data.append(row)
        print(f'lambda_handler loaded {len(data)} rows from file {key}')
        
        # table, products
        load_to_table_products(record_index, from_path, data)
        print(f'lambda_handler record_index = {record_index} from path {from_path}, the function, load_to_table_products is completed')


        # table, branches
        load_to_table_branches(record_index, from_path, data)
        print(f'lambda_handler record_index = {record_index} from path {from_path}, the function, load_to_table_branches is completed')

        # table, payments
        load_to_table_payments(record_index, from_path, data)
        print(f'lambda_handler record_index = {record_index} from path {from_path}, the function, load_to_table_payments is completed')

        # table, orders & table, order_product
        load_to_table_order_n_order_product(record_index, from_path, data)
        print(f'lambda_handler record_index = {record_index} from path {from_path}, the function, load_to_table_order_n_order_product is completed')

        
        
        return 'test is done.'