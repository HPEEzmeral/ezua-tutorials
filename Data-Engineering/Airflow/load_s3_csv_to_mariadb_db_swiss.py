# This DAG downloads a CSV file from MinIO and imports it into MariaDB
#
# This DAG assumes that you have already created the following connections in Airflow:
#   1. s3_connection: A connection to your MinIO instance
#   2. mysql_connection: A connection to your MariaDB instance
#
#
# created by Dirk Derichsweiler & Vincent Charbonnier & Isabelle Steinhauser
# 2023-08-08
#

# Define the AWS credentials and bucket/file information

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import boto3
import pandas as pd
import MySQLdb
import logging
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),  # Set the start date to the current date and time
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the op_kwargs dictionary ADAPT to your EZUA env
op_kwargs = {
    'bucket_name': 'ezaf-demo',
    'file_name': 'Switzerland_sales_data_2019_2023.csv',
    's3_endpoint': 'https://192.168.141.26:31900',
    'access_key': 'minioadmin',
    'secret_key': 'minioadmin',
    'db_host': 'mariadb.mariadb.svc.cluster.local',
    'db_port': '3306',
    'db_user': 'root',
    'db_password': 'Hpepoc@123',
    'db_name': 'discover',
    'table_name': 'swiss'
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
    conn = MySQLdb.connect(
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

# Define the function to run the clean_data.py script
def run_clean_data_script(db_host=None, db_port=None, db_user=None, db_password=None, db_name=None, table_name=None):
    import subprocess

    script_path = "/usr/local/airflow/dags/gitdags/Scripts/clean_data.py"  # ADAPT with the actual path to clean_data.py
    command = [
        "python",
        script_path,
        "-db", "mysql",
        "-H", db_host,
        "-u", db_user,
        "-p", db_password,
        "-P", db_port,
        "-d", db_name,
        "-t", table_name
    ]
    
    subprocess.run(command, check=True)

with DAG('load_s3_csv_to_mariadb_swiss', default_args=default_args, schedule_interval='0 7 * * *') as dag:
    process_csv = PythonOperator(
    task_id='process_csv',
    python_callable=process_csv_file,
    op_kwargs=op_kwargs
    )

    clean_data = PythonOperator(
        task_id='clean_data',
        python_callable=run_clean_data_script,
        op_kwargs=op_kwargs
    )

    process_csv >> clean_data
