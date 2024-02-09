# This DAG downloads a CSV file from MinIO and imports it into MariaDB
#
# This DAG assumes that you have already created the following connections in Airflow:
#   1. s3_connection: A connection to your MinIO instance
#   2. mysql_connection: A connection to your MariaDB instance
#
#
# created by Dirk Derichsweiler 
# 2021-08-31
#

# Define the AWS credentials and bucket/file information


from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import boto3
import pandas as pd
import mysql.connector
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 3),
}

def read_csv_from_s3(bucket_name, file_name, s3_endpoint, access_key=None, secret_key=None):
    s3 = boto3.client(
        's3',
        verify=False,
        endpoint_url=s3_endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    df = pd.read_csv(obj['Body'])
    return df

def import_csv_to_mariadb(df, db_host, db_port, db_user, db_password, db_name, table_name):
    conn = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = conn.cursor()

    # Create table if it doesn't exist
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for column in df.columns:
        # Skip the 'PRICE' column
        if column == 'UNITPRICE' or column == 'TOTALSALES':
            create_table_query += f"{column} FLOAT, "
        else:
            create_table_query += f"{column} VARCHAR(255), "
    create_table_query = create_table_query[:-2] + ")"
    cursor.execute(create_table_query)

    # Convert 'PRICE' column to numeric type
    df['UNITPRICE'] = df['UNITPRICE'].astype(float)

    # Insert data into the table
    insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))})"
    cursor.executemany(insert_query, df.values.tolist())

    conn.commit()
    cursor.close()
    conn.close()

def process_csv_file(bucket_name, file_name, s3_endpoint, access_key=None, secret_key=None,
                     db_host=None, db_port=None, db_user=None, db_password=None, db_name=None, table_name=None):
    df = read_csv_from_s3(bucket_name, file_name, s3_endpoint, access_key, secret_key)

    # Output the headers
    headers = df.columns.tolist()
    logging.info("Headers: %s", headers)

    import_csv_to_mariadb(df, db_host, db_port, db_user, db_password, db_name, table_name)


with DAG('discover_load_s3_csv_to_mariadb_db_czech', default_args=default_args, schedule_interval=None) as dag:
    process_csv = PythonOperator(
        task_id='process_csv',
        python_callable=process_csv_file,
        op_kwargs={
            'bucket_name': 'ezaf-demo',
            'file_name': 'czech.csv',
            's3_endpoint': 'https://home.hpe-dev-ezaf.com:31900',
            'access_key': 'minioadmin',
            'secret_key': 'minioadmin',
            'db_host': 'ddk3s.westcentralus.cloudapp.azure.com',
            'db_port': '31219', 
            'db_user': 'dderichswei',
            'db_password': 'Hpepoc@123',
            'db_name': 'discover',
            'table_name': 'czech'
        }
    )

    process_csv

