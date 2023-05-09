import json
import psycopg2
import boto3

ssm_client = boto3.client('ssm')
parameter_details = ssm_client.get_parameter(Name='mocha-madness-redshift-settings')
redshift_details = json.loads(parameter_details['Parameter']['Value'])
print(f'lambda_handler redshift_details = {redshift_details["host"]}')

dbname = redshift_details['database-name']
user = redshift_details['user']
host = redshift_details['host']
port = redshift_details['port']
password = redshift_details['password']

# Connect to the database
def database_connection(dbname, user, password, host, port):
    conn =  psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    cursor = conn.cursor()
    return conn,cursor

conn, cursor = database_connection(dbname, user, password, host, port)
