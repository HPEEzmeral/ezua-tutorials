#!/bin/bash
echo "Start Reverse Tunnel"
sudo -S ssh -i ~/learning/id_rsa_greenlake.pem dfaasusr@16.103.6.85 -L 9092:localhost:9092 -L 2049:localhost:2049 -L 111:localhost:111 -N -f

echo "Start Producer"
./producer.py -c Germany -cu Euro -s 4 -sy 2022 -ey 2023 -t newtopic
./producer.py -c Germany -cu Euro -s 6 -sy 2019 -ey 2023 -t test4  

echo "Start Consumer"
./consumer.py -s3 https://s3.mydirk.de -s3-key ezua-dev-env -s3-secret fIoHTPuNPi7Kgftzjf2XFO3UNsEmAa2o -b ezuaf -t newtopic -c dirk-newtopic.csv
./consumer.py -s3 https://s3.mydirk.de -s3-key ezua-dev-env -s3-secret fIoHTPuNPi7Kgftzjf2XFO3UNsEmAa2o -b ezuaf -t test5 -c kafka_ezuaf_demo.csv
