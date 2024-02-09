#!/bin/python3
### created by Dirk Derichsweiler

#
# Demo for DF



import csv
import boto3
from io import StringIO
from kafka import KafkaConsumer
import urllib3
urllib3.disable_warnings()
import argparse
import sys


kafka_server='localhost:9092'
kafka_topic="sales_data"
s3_server=""
csv_filename="sales_data.csv"

argParser = argparse.ArgumentParser()
argParser.add_argument("-s3", "--s3server", help="s3 server url")
argParser.add_argument("-s3-key", "--s3key", help="aws_access_key_id")
argParser.add_argument("-s3-secret", "--s3secret", help="aws_secret_access_key")
argParser.add_argument("-k", "--kafkaserver", help="kafka url ex. localhost:9092")
argParser.add_argument("-b", "--bucket", help="define the bucket")
argParser.add_argument("-t", "--topic", help="topic, if you do not specify any topic it will use sales_data")
argParser.add_argument("-c", "--csv", help="csv filename")


args = argParser.parse_args()
print("args=%s" % args)
print("args.topic=%s" % args.topic)
print("args.server=%s" % args.s3server)

if args.topic != None: kafka_topic=args.topic
if args.kafkaserver != None: kafka_server=args.kafkaserver
if args.s3server != None: s3_server=args.s3server
else:
        print("s3 server required")
        sys.exit()

if args.bucket != None: 
        s3_bucket=args.bucket
else:
    print("s3 serverbucket is required")
    sys.exit()

if args.s3key != None:
      s3_key=args.s3key
else:
      print("AWS Access Key is required")
      sys.exit()

if args.csv != None: csv_filename=args.csv
      




# Initialize Kafka consumer
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=[kafka_server],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8')
)


s3 = boto3.resource('s3', verify=False, endpoint_url=s3_server, 
    aws_access_key_id='ezua-dev-env',
    aws_secret_access_key='fIoHTPuNPi7Kgftzjf2XFO3UNsEmAa2o')



# Open CSV file for writing
with open(str(csv_filename), 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    
    # Consume messages from Kafka topic and write to CSV file
    for message in consumer:
        row = message.value.split(',')
        if (row == ['"EOF"']):
            print("EOF recognized.")
            print(str(csv_filename))
            s3.Bucket(s3_bucket).upload_file(str(csv_filename),str(csv_filename))
        print(row)
        writer.writerow(row)