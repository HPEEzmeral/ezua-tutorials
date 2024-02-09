# created by Dirk Derichsweiler
# 
# Ezmeral Unified Analytics Workshop
#
from airflow import DAG
from datetime import datetime, timedelta
import boto3
import json
import pandas as pd
import sys



# Define the AWS credentials and bucket/file information
aws_server_url = 'https://s3.mydirk.de'
aws_access_key_id = 'ezua-dev-env'
aws_secret_access_key = 'fIoHTPuNPi7Kgftzjf2XFO3UNsEmAa2o'
bucket_name = 'ezuaf'
input_file_name = 'kafka_ezuaf_demo.csv'
output_file_name = 'cleaned_kafka_ezuaf_demo.csv'

# Define the function that will read the file from S3, process its contents, and upload the output back to S3
def process_file_and_upload_to_s3():
    # Create an S3 resource object with the specified credentials
    s3 = boto3.resource('s3', verify=False, endpoint_url=aws_server_url, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    # Get the S3 input file object
    input_obj = s3.Object(bucket_name, input_file_name)

    # # Read the contents of the input file
    input_content = input_obj.get()['Body'].read().decode('utf-8')
    
    # Read input file and remove all extra whitespace and quotation marks
    input_content = input_content.replace('""', '"').replace('" "', '').replace('\n', '').replace(': ', '":"').replace(',', '","').replace('""', '"').replace('unit price', 'unit_price').replace('sales', 'total_sales').replace('id', 'product_id').replace('}', '"}').replace('""', '"')
    # Fix syntax errors and add brackets to make it a valid JSON array
    # input_content = '[' + input_content.replace('}"," {', '},\n{')[:-2] + ']]'
    input_content = input_content.replace('"[','[')
    input_content = input_content.replace(']"',']')
    input_content = input_content.replace('"," {',', {')

    df = pd.DataFrame.from_records(json.loads(input_content))    


    print(df.columns)

    # Create an S3 output file object
    output_obj = s3.Object(bucket_name, output_file_name)

    # Write the processed contents to the output file
    output_content = df.to_csv(index=False)
    output_obj.put(Body=output_content)

process_file_and_upload_to_s3()
