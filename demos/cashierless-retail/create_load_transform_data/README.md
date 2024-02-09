# ------------------------------------------------------------------------
# create_csv.py
# ------------------------------------------------------------------------
This script generates sales data for a specified country and time period, and saves it as a CSV file. The user can specify the CSV filename, the country, the currency, the number of stores to generate sales data for, and the start and end year for the sales data.

## Prerequisites
- Python 3.x
- `pycountry` library (`pip install pycountry`)
- `fuzzywuzzy` library (`pip install fuzzywuzzy`)
- `requests` library (`pip install requests`)

## Usage
- `python generate_sales_data.py [-csv CSV_FILE] [-c COUNTRY] [-cu CURRENCY] [-s STORES] [-sy START_YEAR] [-ey END_YEAR]`

## Arguments
- `-csv, --csvfile`: Allows the user to specify a filename for the CSV file to be created. If not specified, it will default to Country_sales_data.csv.
- `-c, --country`: Allows the user to specify a country name. If not specified, it will default to Germany.
- `-cu, --currency`: Allows the user to specify a currency code. If not specified, it will default to EUR.
- `-s, --stores`: Allows the user to specify the number of stores to generate sales data for. If not specified, it will default to 1.
- `-sy, --startyear`: Allows the user to specify the starting year for the sales data. If not specified, it will default to 2023.
- `-ey, --endyear`: Allows the user to specify the ending year for the sales data. If not specified, it will default to 2023.
- `-p, --path`: Allows the user to specify the path where the CSV file will be created. If not specified, it will default to the current directory followed by /data/

## Example
- `python create_csv.py -csv czech_sales_data_2019_2023.csv -c "Czech Republic" -cu CZK -s 5 -sy 2019 -ey 2023`

# ------------------------------------------------------------------------
# import_data.py
# ------------------------------------------------------------------------
This script generates sales data for a specified country and time period, and saves it as a CSV file. The user can specify the CSV filename, the country, the currency, the number of stores to generate sales data for, and the start and end year for the sales data.

## Prerequisites
- Python 3.x
- `mysql-connector-python` library (`pip install mysql-connector-python`)
- `psycopg2` library (`pip install psycopg2`)
- A SQL server with a database and credentials to connect to it

## Usage
`python import_data.py -db <db_type> -H <hostname> -u <username> -p <password> -P <port> -d <database> -t <table> -c <csv_file>`

## Arguments
- `-db, --database_type`: Type of SQL database (e.g. mysql, postgresql) (required)
- `-H, --host`: SQL hostname (required)
- `-u, --user`: SQL username (required)
- `-p, --password`: SQL password (required)
- `-P, --port`: SQL port (required)
- `-d, --database`: SQL database name (required)
- `-t, --table`: SQL table name (required)
- `-c, --csv`: CSV filename (required)

## Example
`python import_data.py -db mysql -H ddk3s.westcentralus.cloudapp.azure.com -u root -p nfWCEHWNDe -P 31870 -d db_g1 -t sales_data -c ../czech_sales_data_2019_2023.csv`

# ------------------------------------------------------------------------
# clean_data.py
# ------------------------------------------------------------------------
This is a Python script named "clean_data.py" that creates a sales data CSV file for a specified country, currency, number of stores, and time period. The generated data is based on a list of pre-defined products and random sales quantities.

## Prerequisites
- Python 3.x
- `mysql-connector-python` library (`pip install mysql-connector-python`)
- `psycopg2` library (`pip install psycopg2`)
- A SQL server with a database and credentials to connect to it
- `pycountry` library (`pip install pycountry`)
- `fuzzywuzzy` library (`pip install fuzzywuzzy`)
- `requests` library (`pip install requests`)argparse

## Usage
`python clean_data.py -db <db_type> -H <hostname> -u <username> -p <password> -P <port> -d <database> -t <table>`

## Arguments
- `-db, --database_type`: Type of SQL database (e.g. mysql, postgresql) (required)
- `-H, --host`: SQL hostname (required)
- `-u, --user`: SQL username (required)
- `-p, --password`: SQL password (required)
- `-P, --port`: SQL port (required)
- `-d, --database`: SQL database name (required)
- `-t, --table`: SQL table name (required)

## Example
`python clean_data.py -db mysql -H ddk3s.westcentralus.cloudapp.azure.com -u root -p nfWCEHWNDe -P 31870 -d db_g1 -t sales_data`