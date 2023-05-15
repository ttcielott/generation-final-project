import boto3
import csv
from io import StringIO
from CSV_transformer.functions_transformation import *

s3 = boto3.client('s3')


def lambda_handler(event, context):
    print(f'lambda_handler started event collected is {event}')

    # Get the object from the event
    print(f'lambda_handler called, event = {event}')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(f'lambda_handler bucket = {bucket}, key = {key}')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        #print(f'lambda_handler s3 response = {response}')
        content = response['Body'].read().decode('utf-8')
        #print(f'lambda_handler s3 content = {content}')
    
        # Read the csv file
        data = read_csv(StringIO(content))
        print(f'lambda_handler loaded {len(data)} rows from file {key}')
        
        #changing the key to only return the name of the store
        store = key.split('/')[-1].split('_')[0]
    except Exception as e:
        print(f'Error in lambda_handler = ${e}')    

        
        