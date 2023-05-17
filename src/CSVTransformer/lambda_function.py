import boto3
import csv
import json
from io import StringIO
from CSVTransformer.functions_transformation import *

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print(f'lambda_handler started event = {event}')
    try:
        for msg_no, msg in enumerate(event['Records']):
            print(f'lambda_handler: msg_no = {msg_no}')
            message_body = msg['body']
            msg_body_json = json.loads(message_body)
            print(f'lambda_handler: msg_body_json loaded okay')
            bucket = msg_body_json['Records'][0]['s3']['bucket']['name']
            key = msg_body_json['Records'][0]['s3']['object']['key']
            print(f'lambda_handler: bucket = {bucket} and key = {key}')
    
            
            response = s3.get_object(Bucket=bucket, Key=key)
            print(f'lambda_handler got s3 response for key = {key}')
            content = response['Body'].read().decode('utf-8')
            print(f'lambda_handler loaded s3 content for key = {key}')
        
            # Read the csv file
            data = read_csv(StringIO(content))
            print(f'lambda_handler loaded {len(data)} rows from file for key = {key}')
            
            #changing the key to only return the name of the store
            store = key.split('/')[-1].split('_')[0]
            print(f'lambda_handler found store = {store} for key = {key}')
    
            # Transform the data
            transformed_data = transform_branch_file(data)
            print(f'lambda_handler transform_data rows = {len(transformed_data)} for file {store}')
            
            
            # Write the transformed data to a new csv file
            print(f'lambda_handler creating output file for store = {store} and key = {key}')
            output = StringIO()
            writer = csv.writer(output)
            writer.writerows(transformed_data)
            
            # Store the transformed csv file in a new bucket
            tranformed_bucket = 'mocha-madness-transformed-data-v2'
            s3.put_object(Body=output.getvalue(), Bucket= tranformed_bucket, Key=key)
            print(f'lambda_handler saved file key = {key} in bucket = {tranformed_bucket}')
            
            # Create SQS client
            sqs = boto3.client('sqs')
            queue_name = 'mocha-madness-redshift-loader-queue'
            queue_url = f'https://sqs.eu-west-1.amazonaws.com/015206308301/{queue_name}'
            message_json = {'bucket': tranformed_bucket, 'key': key}
            # covert into json string
            message_text = json.dumps(message_json)
            
            print(f'lambda_handler sending message to {queue_name} for key = {key}')
            
            # Send message to SQS queue
            response = sqs.send_message(
                QueueUrl= queue_url,
                DelaySeconds=10,
                MessageBody=(message_text)
            )
            print(f'lambda_handler sent message to {queue_name} for key = {key}')
    
            print(f'lambda_handler finished for key = {key}')
    
    except Exception as e:
        print(f'Error in lambda_handler = {e}')