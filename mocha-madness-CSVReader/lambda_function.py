import boto3
import csv
from io import StringIO
from functions_transformation import *

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
        
        # Transform the data
        #transformed_data = transform_data(data)
        transformed_data = transform_branch_file(data)
        print(f'lambda_handler transform_data rows = {len(transformed_data)} for file {store}')
        
        
        # Write the transformed data to a new csv file
        print(f'lambda_handler creating output file = {store}')
        output = StringIO()
        writer = csv.writer(output)
        writer.writerows(transformed_data)
        
        # Store the transformed csv file in a new bucket
        s3.put_object(Body=output.getvalue(), Bucket='mocha-madness-transformed-data', Key=key)
        print(f'lambda_handler finished processing file {key}')
    except Exception as e:
        print(f'Error in lambda_handler = ${e}')
    
