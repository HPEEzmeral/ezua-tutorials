#!/bin/python3
"""
EZUAF DEMO
created Vincent Charbonnier, 2023
clean fruit&veg dataset in SQL DBs
"""

import subprocess

# List of libraries to install
libraries_to_install = ["fuzzywuzzy", "pycountry", "python-Levenshtein"]

# Run the pip command to install the libraries
for library in libraries_to_install:
    try:
        subprocess.run(["pip", "install", library], check=True)
        print(f"{library} library installed successfully.")
    except subprocess.CalledProcessError:
        print(f"Failed to install {library} library.")

# import the necessary libraries
from fuzzywuzzy import process
import pycountry
import requests
import sys
import argparse
import logging

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
args = parser.parse_args()
if args.database_type != None: db_type=args.database_type 
else:
    print("hostname required")
    sys.exit()
if args.host != None: db_host=args.host 
else:
    print("hostname required")
    sys.exit()
if args.user != None: db_user=args.user
else:
    print("username is required")
    sys.exit()
if args.password != None: db_password=args.password
else:
    print("password is required")
    sys.exit()
if args.database != None: db_name=args.database
else:
    print("database name is required")
    sys.exit()
if args.table != None: table_name=args.table
else:
    print("table name is required")
    sys.exit()
if args.port != None: db_port=args.port
else:
    print("port name is required")

# Define a minimum match score for fuzzy matching
MIN_MATCH_SCORE = 70

# Define a function to validate the country name using fuzzy matching
def validate_country_name_fuzzy(country_name):
    countries = [c.name for c in pycountry.countries]
    match = process.extractOne(country_name, countries)
    if match[1] >= MIN_MATCH_SCORE:
        country = pycountry.countries.get(name=match[0])
        return country.alpha_2
    else:
        return None

# Define a function to validate the currency code using fuzzy matching
def validate_currency_code(currency_code):
    currencies = [c.alpha_3 for c in pycountry.currencies]
    match = process.extractOne(currency_code, currencies)
    if match[1] >= MIN_MATCH_SCORE:
        return match[0]
    else:
        return None

def get_currency_code(country_name):
    """
    Given a country name, returns its currency code using pycountry library.
    If the country name is not found, returns None.
    """
    try:
        country_code = pycountry.countries.search_fuzzy(country_name)[0].alpha_3
        if country_code in ['AUT', 'BEL', 'CYP', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'IRL', 'ITA', 'LVA', 'LTU', 'LUX', 'MLT', 'NLD', 'PRT', 'SVK', 'SVN', 'ESP']:
            return 'EUR'
        currency_code = pycountry.currencies.get(numeric=pycountry.countries.get(alpha_3=country_code).numeric).alpha_3
        return currency_code
    except LookupError:
        print(f"E: Could not find currency for country {country_name}")
        return None

def get_database_connection(database_type):
    """
    Given the database type, returns a connection to the database.
    If the database type is not supported, returns None.
    """
    if database_type == "mysql":
        # Define the MySQL database parameters
        host = db_host
        user = db_user
        password = db_password
        database = db_name
        table = table_name
        port = db_port

        # Connect to the MySQL database
        print("# Connecting to the MySQL database...")
        try:
            import MySQLdb
        except ImportError:
            print("Error: MySQLdb library not found. Please install it using pip.")
            sys.exit()

        cnx = MySQLdb.Connection(user=user, password=password,
                                 host=host, port=int(port), database=database)
        return cnx
    elif database_type == "postgresql":
        # Define the PostgreSQL database parameters
        host = db_host
        user = db_user
        password = db_password
        database = db_name
        table = table_name
        port = db_port

        # Connect to the PostgreSQL database
        print("# Connecting to the PostgreSQL database...")
        try:
            import psycopg2
        except ImportError:
            print("Error: psycopg2 library not found. Please install it using pip.")
            sys.exit()

        cnx = psycopg2.connect(host=host, port=port, user=user, 
                               password=password, database=database)
        return cnx
    else:
        print("Error: Unsupported database type.")
        return None

def execute_query(cursor, query, params=None):
    """
    Given a cursor, a query, and optional parameters, executes the query and returns the result.
    If an error occurs, prints an error message and returns None.
    """
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def update_database_table(database_type, database, table):
    # Create a connection to the database
    cnx = get_database_connection(database_type)
    if cnx is None:
        return
                               
    # Create a cursor to execute SQL queries
    cursor = cnx.cursor()

    # Read the database table
    print(f"# Reading the {database_type} database table {database}.{table}...")
    query = f"SELECT * FROM {table}"
    rows = execute_query(cursor, query)

    # Define the API endpoint for fetching the latest exchange rates
    exchange_rate_api_endpoint = "https://api.exchangerate-api.com/v4/latest/EUR"

    # Fetch the latest exchange rates from the API
    print("# Fetching the latest exchange rates from the API...")
    response = requests.get(exchange_rate_api_endpoint)
    if response.status_code == 200:
        exchange_rates = response.json().get("rates")
    else:
        # Handle the case where the API request fails
        print("Error: Unable to fetch exchange rates from API")
        exit()

    # Iterate over the rows and validate the country names
    print("# Analyzing the data...")
    updated_rows = []
    for row in rows:
        country = str(row[9])
        curr_code = str(row[7])
        # Validate the country name and get the currency code
        try:
            country_obj = pycountry.countries.search_fuzzy(country)[0]
            country_name = country_obj.official_name
            currency_code = get_currency_code(country_name)
        except LookupError:
            print(f"E: Could not find currency for country {country_name}")
            continue

        # If the currency code is already EUR, add the row to updated_rows without performing any currency conversion
        if curr_code == "EUR":
            updated_rows.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], country_name, row[10]))
        else:
            # Convert the currency value to EUR using the exchange rate
            currency_rate = exchange_rates.get(currency_code)
            
            if currency_rate is not None:
                currency_code = "EUR"

                # Convert row[3] and row[5] to float
                try:
                    unitprice = float(row[3])
                    quantity = float(row[5])
                except ValueError:
                    print("Error: Unable to convert to numeric value for multiplication.")
                    continue  # Skip this iteration and move to the next row

                # Calculate the unit price in Euro
                unit_euro = unitprice / currency_rate

                # Calculate the total sales and round to two decimal places
                totalsales = unit_euro * quantity

                updated_rows.append((row[0], row[1], row[2], unit_euro, row[4], quantity, totalsales, currency_code, row[8], country_name, row[10]))

    # Write the corrected data back to the database table
    print(f"# Updating the {database_type} database table {db_name}.{table_name} with validated country names and currencies...")
    query = f"TRUNCATE TABLE {table}"
    cursor.execute(query)
    query = f"INSERT INTO {table} (productid, product, type, unitprice, unit, qty, totalsales, currency, store, country, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, updated_rows)
    cnx.commit()

    # Get details from the database cursor
    cursor.execute(f"SELECT * FROM {table} LIMIT 10")
    column_names = [column[0] for column in cursor.description]
    results = cursor.fetchall()

    # Print the results from the database
    print(f"# Results from the {database_type} database {db_name}:")
    print(column_names)
    for result in results:
        print(result)

    # Close the database connection
    cnx.close()
    print(f"# Done updating {db_type} database {db_name}.")

# Call the function to update the SQL database
update_database_table(db_type, db_name, table_name)
