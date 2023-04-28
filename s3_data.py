import boto3
import csv
from io import StringIO

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    input_bucket_name = event['Records'][0]['s3']['bucket']['name']
    input_file_name = event['Records'][0]['s3']['object']['key']
    
    # Read the content of the CSV file
    csvfile = s3.get_object(Bucket=input_bucket_name, Key=input_file_name)
    csvcontent = csvfile['Body'].read().decode('utf-8')
    
    # Transform the data
    transformed_data = []
    reader = csv.reader(StringIO(csvcontent))
    for row in reader:
        # Remove the name and card columns
        del row[2]
        del row[5]
        
        # Perform some transformation on the data
        transformed_row = [cell.upper() for cell in row]
        transformed_data.append(transformed_row)
    
    # Write the transformed data to a new CSV file in another S3 bucket
    output_bucket_name = 'mocha-madness-transformed-data'
    output_file_name = input_file_name + '_transformed'
    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(transformed_data)
    
    s3.put_object(Body=output.getvalue(), Bucket=output_bucket_name, Key=output_file_name)