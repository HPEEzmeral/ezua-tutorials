#!/bin/python3
### created by Dirk Derichsweiler+
#
# Demo for DF
import random
import csv
from kafka import KafkaProducer
import json
import argparse
import sys

country = 'Austria'
currency = 'EUR'
kafka_server='localhost:9092'
kafka_topic="sales_data"
store_amount = 1
start_year = 2023
end_year = 2023

argParser = argparse.ArgumentParser()
argParser.add_argument("-c", "--country", help="if you do not specify, we will use GERMANY as default")
argParser.add_argument("-cu", "--currency", help="if you do not specify, we will use EURO as default")
argParser.add_argument("-k", "--kafkaserver", help="kafka url ex. localhost:9092")
argParser.add_argument("-t", "--topic", help="topic, if you do not specify any topic it will use sales_data")
argParser.add_argument("-s", "--stores", help="amount of stores, if you do not specify 1 store will be created")
argParser.add_argument("-sy", "--startyear", help="start year")
argParser.add_argument("-ey", "--endyear", help="end year")



args = argParser.parse_args()
if args.country != None: kafka_topic=args.country
if args.currency != None: currency = args.currency
if args.topic != None: kafka_topic=args.topic
if args.kafkaserver != None: kafka_server=args.kafkaserver
if args.stores != None: store_amount=args.stores
if args.startyear != None: start_year=args.startyear
if args.endyear != None: end_year=args.endyear

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
        {"id": 36, "name": "eggplant", "type": "vegetables", "unit_price": 1.5, "unit": "kg"}
]

# Generate sales data for the last 5 years for 5 stores
# stores = ["Store A", "Store B", "Store C", "Store D", "Store E"]
# years = [2018, 2019, 2020, 2021, 2022]
stores = []
years = []

if int(start_year) > int(end_year):
    print("E: start_year is higher then end year")
    sys.exit()

amount_of_years = int(end_year) - int(start_year)

x=0
while(x < int(amount_of_years+1)):
    years.append(str(int(start_year)+int(x)))
    x=x+1
print(years) 


# x = chr(ord('A') + 3)
x=0
while( x < int(store_amount)):

    char = chr(ord('A') + x )
    x=x+1
    stores.append("Store "+char)

# Sales data will be stored in a list of dictionaries
sales_data = []

for year in years:
    for store in stores:
        total_sales = 0

        # Generate sales data for vegetables
        for product in products:
            quantity = random.randint(50, 2000) # Generate a random quantity between 50 and 200 kg
            total_sales += quantity * product["unit_price"]

            # Add sales data to the list
            sales_data.append({
                "id": product["id"],
                "product": product["name"],
                "type": product["type"],
                "unit price": product["unit_price"],
                "unit": product["unit"],
                "qty": quantity,
                "sales": round(total_sales, 2),
                "currency": currency,
                "store": store,
                "country": country,
                "year": year
            })

# Define the Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers=[kafka_server],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

producer.send(kafka_topic, value=sales_data)
producer.send(kafka_topic, "EOF")
producer.flush()