#!/bin/bash

sed -e "s/\$AUTH_TOKEN/$AUTH_TOKEN/" /mnt/usr/ezua-tutorials/Data-Analytics/Spark/object_store_secret.yaml.tpl > /tmp/object_store_secret.yaml
kubectl apply -f /tmp/object_store_secret.yaml
