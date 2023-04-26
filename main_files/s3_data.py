import csv
from databaseconn_main import *
import boto3
import os 


# Get AWS login information from .env file - will need to be unique I believe for all team members
load_dotenv('../database/.env')

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')

conn, cur = database_connection(dbname, user, password, host, port)

# connect to the AWS bucket
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
bucket_name = 'mocha-madness-raw-data'


# Lists all files stored in the path Amazon S3 Buckets mocha-madness-raw-data 2023/ 4/ 26/
csv_files = []
for obj in s3.list_objects(Bucket=bucket_name, Prefix='2023/4/26/')['Contents']:
    if obj['Key'].endswith('.csv'):
        csv_files.append(obj['Key'])

# Now to work with each csv file and transform the data and insert it into orders table
for csv_file in csv_files:
    s3.download_file(bucket_name, csv_file, '/tmp/temp.csv')

    with open('/tmp/temp.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cur.execute(
            """"
            INSERT INTO orders (date, time, branch_id, product_name, size, product_price, total_price, payment_method_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, row)
conn.commit()
cur.close()
conn.close()

