#!/bin/python3
"""
HPE Ezmeral Unified Analytics - Create Synthetic Retail Store CSV Data 
Created by Dirk Derichsweiler & Vincent Charbonnier, 2023
Modified by Alex Ollman, 2024
"""

import random
import csv
import argparse
import sys
import pycountry
from fuzzywuzzy import process
import requests
import os
import getpass
import json

# Set default values in case nothing was selected
country = 'Germany'
currency = 'EUR'
store_amount = 1
start_year = 2023
end_year = 2023

# Define constant variables
EXCHANGE_RATE_API_ENDPOINT = "https://api.exchangerate-api.com/v4/latest/EUR"  # API endpoint for fetching exchange rates

# Defines an argparse object called argParser to parse the command-line arguments.
argParser = argparse.ArgumentParser()
argParser.add_argument("-csv", "--csvfile", help="Allows the user to specify a filename for the CSV file to be created. If not specified, it will default to Country_sales_data.csv.")
argParser.add_argument("-c", "--country", help="Allows the user to specify a country name. If not specified, it will default to Germany.")
argParser.add_argument("-cu", "--currency", help="Allows the user to specify a currency code. If not specified, it will default to EUR.")
argParser.add_argument("-s", "--stores", help="Allows the user to specify the number of stores to generate sales data for. If not specified, it will default to 1.")
argParser.add_argument("-sy", "--startyear", help="Allows the user to specify the starting year for the sales data. If not specified, it will default to 2023.")
argParser.add_argument("-ey", "--endyear", help="Allows the user to specify the ending year for the sales data. If not specified, it will default to 2023.")
argParser.add_argument("-p", "--path", help="Allows the user to specify the path where the CSV file will be created. If not specified, it will default to the current directory followed by /data/")

# Parse the command-line arguments using the argparse object and 
# If a specific argument is passed, update the corresponding variable in the program with the new value.
args = argParser.parse_args()
if args.csvfile != None: csv_file = args.csvfile
if args.country != None: country = args.country
if args.currency != None: currency = args.currency
if args.stores != None: store_amount = args.stores
if args.startyear != None: start_year = args.startyear
if args.endyear != None: end_year = args.endyear
if args.path != None:
    path = args.path
else:
    path = "./data/"

    if not os.path.exists(path):
        os.makedirs(path)

if args.csvfile != None: 
    # Get the current user
    current_user = getpass.getuser()
    
    # Define the directory path
    directory = f"/mnt/shared/retail-data/raw-data/"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    csv_file = directory + args.csvfile
else: 
    csv_file = path + country + "_sales_data_" + str(start_year) + "_" + str(end_year) + ".csv"

# Define the products
products = [
        {"id": 1, "name": "banana", "type": "fruits", "unit_price": 0.5, "unit": "kg"},
        {"id": 2, "name": "apple", "type": "fruits", "unit_price": 0.7, "unit": "kg"},
        {"id": 3, "name": "pear", "type": "fruits", "unit_price": 0.6, "unit": "kg"},
        {"id": 4, "name": "grapes", "type": "fruits", "unit_price": 1.2, "unit": "kg"},
        {"id": 5, "name": "orange", "type": "fruits", "unit_price": 0.8, "unit": "kg"},
        {"id": 6, "name": "kiwi", "type": "fruits", "unit_price": 0.9, "unit": "piece"},
        {"id": 7, "name": "watermelon", "type": "fruits", "unit_price": 5.0, "unit": "kg"},
        {"id": 8, "name": "pomegranate", "type": "fruits", "unit_price": 2.5, "unit": "kg"},
        {"id": 9, "name": "pineapple", "type": "fruits", "unit_price": 1.5, "unit": "piece"},
        {"id": 10, "name": "mango", "type": "fruits", "unit_price": 2.0, "unit": "piece"},
        {"id": 11, "name": "cucumber", "type": "vegetables", "unit_price": 0.4, "unit": "piece"},
        {"id": 12, "name": "carrot", "type": "vegetables", "unit_price": 0.3, "unit": "kg"},
        {"id": 13, "name": "capsicum", "type": "vegetables", "unit_price": 0.5, "unit": "kg"},
        {"id": 14, "name": "onion", "type": "vegetables", "unit_price": 0.2, "unit": "kg"},
        {"id": 15, "name": "potato", "type": "vegetables", "unit_price": 0.3, "unit": "kg"},
        {"id": 16, "name": "lemon", "type": "vegetables", "unit_price": 0.4, "unit": "kg"},
        {"id": 17, "name": "tomato", "type": "vegetables", "unit_price": 0.6, "unit": "kg"},
        {"id": 18, "name": "raddish", "type": "vegetables", "unit_price": 0.3, "unit": "kg"},
        {"id": 19, "name": "beetroot", "type": "vegetables", "unit_price": 0.4, "unit": "kg"},
        {"id": 20, "name": "cabbage", "type": "vegetables", "unit_price": 0.5, "unit": "piece"},
        {"id": 21, "name": "lettuce", "type": "vegetables", "unit_price": 0.6, "unit": "piece"},
        {"id": 22, "name": "spinach", "type": "vegetables", "unit_price": 0.7, "unit": "kg"},
        {"id": 23, "name": "soy bean", "type": "vegetables", "unit_price": 0.8, "unit": "kg"},
        {"id": 24, "name": "cauliflower", "type": "vegetables", "unit_price": 0.6, "unit": "piece"},
        {"id": 25, "name": "bell pepper", "type": "vegetables", "unit_price": 0.7, "unit": "kg"},
        {"id": 26, "name": "chilli pepper", "type": "vegetables", "unit_price": 0.5, "unit": "kg"},
        {"id": 27, "name": "turnip", "type": "vegetables", "unit_price": 0.4, "unit": "kg"},
        {"id": 28, "name": "corn", "type": "vegetables", "unit_price": 0.3, "unit": "kg"},
        {"id": 29, "name": "sweetcorn", "type": "vegetables", "unit_price": 0.4, "unit": "kg"},
        {"id": 30, "name": "sweet potato", "type": "vegetables", "unit_price": 0.5, "unit": "kg"},
        {"id": 31, "name": "paprika", "type": "vegetables", "unit_price": 2.0, "unit": "kg"},
        {"id": 32, "name": "jalepeno", "type": "vegetables", "unit_price": 2.0, "unit": "kg"},
        {"id": 33, "name": "ginger", "type": "vegetables", "unit_price": 1.5, "unit": "kg"},
        {"id": 34, "name": "garlic", "type": "vegetables", "unit_price": 1.5, "unit": "kg"},
        {"id": 35, "name": "peas", "type": "vegetables", "unit_price": 3.0, "unit": "kg"},
        {"id": 36, "name": "eggplant", "type": "vegetables", "unit_price": 1.5, "unit": "kg"},
        {"id": 37, "name": "garden hose", "type": "gardening", "unit_price": 15.0, "unit": "piece"},
        {"id": 38, "name": "masking tape", "type": "crafting", "unit_price": 2.5, "unit": "piece"},
        {"id": 39, "name": "paint", "type": "crafting", "unit_price": 10.0, "unit": "liter"},
        {"id": 40, "name": "ice remover spray", "type": "winter", "unit_price": 8.0, "unit": "bottle"},
        {"id": 41, "name": "ezmeral", "type": "jewelry", "unit_price": 1, "unit": "piece"},
        {"id": 42, "name": "steel nail", "type": "hardware", "unit_price": 0.1, "unit": "piece"},
        {"id": 43, "name": "square board", "type": "woodworking", "unit_price": 5.0, "unit": "piece"},
        {"id": 44, "name": "meter", "type": "tools", "unit_price": 20.0, "unit": "piece"},
        {"id": 45, "name": "paintbrush", "type": "crafting", "unit_price": 3.0, "unit": "piece"},
        {"id": 46, "name": "hammer", "type": "tools", "unit_price": 12.0, "unit": "piece"}
]

# Create empty lists to store store names and years
stores = []
years = []

# Check if start_year is greater than end_year
# If True, print an error message and exit the program
if int(start_year) > int(end_year):
    print("E: Start_year is higher then end year")
    sys.exit()

# Calculate the number of years between start_year and end_year, and add the years to the years list
amount_of_years = int(end_year) - int(start_year)
x=0
while(x < int(amount_of_years+1)):
    years.append(str(int(start_year)+int(x)))
    x=x+1

# Generate store names based on the number of stores specified by the user
# The names will be in the format "Store A", "Store B", etc.
x=0
while( x < int(store_amount)):
    char = chr(ord('A') + x )
    x=x+1
    stores.append("Store "+char)


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

# Sales data will be stored in a list of dictionaries
sales_data = []

# Variables Selected
print("# Variables Selected")
print(f"\t- Country: {country}")
print(f"\t- Currency: {currency}")
print(f"\t- Stores: {store_amount}")
print(f"\t {stores}")
print(f"\t- Start: {start_year}")
print(f"\t- End: {end_year}")

# Validate the country name and get the currency code
try:
    country_obj = pycountry.countries.search_fuzzy(country)[0]
    country_name = country_obj.official_name
    currency_code = get_currency_code(country_name)
except LookupError:
    sys.exit()

    
def read_json_file(file_name):
    try:
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the full path to the JSON file
        file_path = os.path.join(script_dir, file_name)
        
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_name}' not found in the directory.")
            return
        
        # Read the JSON file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            # Check if "rates" field exists in the JSON data
            if "rates" in data:
                return data["rates"]
            else:
                print("Error: 'rates' field not found in the JSON file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    
# Fetch the latest exchange rates from the API
try:
    response = requests.get(EXCHANGE_RATE_API_ENDPOINT)
    if response.status_code == 200:
        exchange_rates = response.json().get("rates")
except:
    print("Exchange API unreachable. Getting conversion rates from local file.")
    exchange_rates = read_json_file('currency_conversion.json')

accelerator=1
if country_obj.name=='Germany':
    accelerator=15
else:
    if country_obj.name=='Switzerland': 
        accelerator=5
    
# Loop through years and stores
for year in years:
    for store in stores:
        # Set a seed based on year and store
        seed = hash(f"{year}_{store}") % (2**32 - 1)
        random.seed(seed)

        total_sales = 0
        sales_data_per_year = []

        # Generate sales data for vegetables
        for product in products:
            # Use the same seed for each product
            random.seed(seed)

            # Calculate the desired total sales range for the product
            min_total_sales = 50000
            max_total_sales = 1000000

            # Calculate a quantity that ensures the total sales fall within the desired range
            unit_price = product["unit_price"] * exchange_rates[currency_code]
            max_quantity = max_total_sales / unit_price
            min_quantity = min_total_sales / unit_price
            quantity = random.randint(int(min_quantity), int(max_quantity))

            # Calculate the total sales for this product
            total_sales += quantity * unit_price

            # Add sales data for this product to the list for this year and store
            sales_data_per_year.append({
                "id": product["id"],
                "product": product["name"],
                "type": product["type"],
                "unit price": unit_price,
                "unit": product["unit"],
                "qty": quantity,
                "sales": round(total_sales, 2),
                "currency": currency,
                "store": store,
                "country": country,
                "year": str(year)
            })

        # Add the sales data for this year and store to the main sales data list
        sales_data.extend(sales_data_per_year)

# Write the data to a CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['PRODUCTID', 'PRODUCT', 'TYPE', 'UNITPRICE', 'UNIT', 'QTY', 'TOTALSALES', 'CURRENCY', 'STORE', 'COUNTRY', 'YEAR'])
    for item in sales_data:
        writer.writerow([item['id'], item['product'], item['type'], item['unit price'], item['unit'], item['qty'], item['sales'], item['currency'], item['store'], item['country'], str(item['year'])])
        
print(f"# File {csv_file} created")
with open(csv_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for i, row in enumerate(csvreader):
        if i == 10:
            break
        print(row)
