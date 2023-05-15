import boto3
import csv
from io import StringIO
from CSV_transformer.functions_transformation import *

s3 = boto3.client('s3')


def lambda_handler(event, context):
    print(f'lambda_handler started event collected is {event}')

    try:
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
        s3.put_object(Body=output.getvalue(), Bucket='mocha-madness-transformed-data-v2', Key=key)
        print(f'lambda_handler finished processing file {key}')
    except Exception as e:
        print(f'Error in lambda_handler = ${e}')
    
