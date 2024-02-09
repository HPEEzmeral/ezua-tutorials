#!/usr/bin/env python3

"""
EZUAF DEMO
created by Dirk Derichsweiler & Vincent Charbonnier, 2023
import CSV to MySQL/MariaDB/PostgreSQL
"""

import argparse
import csv
import logging
import mysql.connector
from mysql.connector import errors
import pandas as pd
import psycopg2

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-db", "--database_type", help="Type of SQL database (e.g. mysql, postgresql)", required=True)
parser.add_argument("-H", "--host", help="SQL hostname", required=True)
parser.add_argument("-u", "--user", help="SQL username", required=True)
parser.add_argument("-p", "--password", help="SQL password", required=True)
parser.add_argument("-P", "--port", help="SQL port", default=3306, type=int)
parser.add_argument("-d", "--database", help="SQL database name", required=True)
parser.add_argument("-t", "--table", help="SQL table name", required=True)
parser.add_argument("-c", "--csv", help="CSV filename", required=True)
args = parser.parse_args()
if args.database_type != None: db_type=args.database_type 
else:
    print("hostname required")
    sys.exit()
if args.host != None: mysql_hostname=args.host 
else:
    print("hostname required")
    sys.exit()
if args.user != None: mysql_username=args.user
else:
    print("username is required")
    sys.exit()
if args.password != None: mysql_password=args.password
else:
    print("password is required")
    sys.exit()
if args.database != None: mysql_database=args.database
else:
    print("database name is required")
    sys.exit()
if args.csv != None: csv_filename=args.csv
else:
    print("CSV filename is required")
    sys.exit()
if args.table != None: mysql_table=args.table
else:
    print("table name is required")
    sys.exit()
if args.port != None: mysql_port=args.port
else:
    print("port name is required")
try:
    if args.database_type.lower() == 'mysql':
        conn = mysql.connector.connect(
            host=args.host,
            user=args.user,
            password=args.password,
            port=args.port,
            database=args.database
        )
    elif args.database_type.lower() == 'postgresql':
        conn = psycopg2.connect(
            host=args.host,
            user=args.user,
            password=args.password,
            port=args.port,
            database=args.database
        )
    else:
        raise ValueError("Invalid database type")
except (errors.Error, ValueError) as e:
    logger.error("Failed to connect to host: %s", e)
    exit(1)

# Create table if not exist 
print(f"# Create table {mysql_table}...")
try:
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS {} (
        product_id INTEGER,
        product TEXT,
        type TEXT,
        unit_price FLOAT,
        unit TEXT,
        qty INTEGER,
        total_sales FLOAT,
        currency TEXT,
        store TEXT,
        country TEXT,
        year INTEGER
    )
    """.format(args.table)
    
    if args.database_type.lower() == 'mysql':
        create_table_query += "ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;"
    elif args.database_type.lower() == 'postgresql':
        create_table_query += ";"
        
    cursor.execute(create_table_query)
    conn.commit()
except errors.Error as e:
    logger.error("Failed to create table: %s", e)
    conn.rollback()
    conn.close()
    exit(1)

    
# Read CSV file using pandas
df = pd.read_csv(csv_filename)

# Loop through rows of dataframe and insert into MariaDB
print("# Import dataset...")
for index, row in df.iterrows():
    print("- " + str(index) + " from " + str(len(df)))
    sql = "INSERT INTO " + mysql_table + " (product_id, product, type, unit_price, unit, qty, total_sales, currency, store, country, year) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s)"
    values = (row['PRODUCT_ID'],row['PRODUCT'],row['TYPE'],row['UNIT PRICE'],row['UNIT'],row['QTY'],row['TOTAL SALES'],row['CURRENCY'],row['STORE'],row['COUNTRY'],row['YEAR'])
    cursor.execute(sql, values)
    conn.commit()
    
print(f"# Data successfully imported to database {mysql_table}...")

# Get details from the MySQL cursor
cursor.execute(f"SELECT * FROM {mysql_table} LIMIT 10")
mysql_column_names = [column[0] for column in cursor.description]
mysql_results = cursor.fetchall()

# Print the results from the MySQL database
print(f"# Results from {mysql_database}.{mysql_table}:")
print(mysql_column_names)
for result in mysql_results:
    print(result)
      
# Commit changes and close connection
conn.commit()
conn.close()