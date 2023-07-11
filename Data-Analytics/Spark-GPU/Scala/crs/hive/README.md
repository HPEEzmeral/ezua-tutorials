### Hive scala examples for Apache spark-3.3.1

Source code for these examples can be found in 'apps' folder.

### Configurations for running the example -

1. If you built the jar file from the source code -
   a) Rename the jar file to - `spark-hive-example-3.3.1.jar`
   b) Place this jar file in - `opt/spark/examples/jars`
   c) Create the image from Dockerfile (spark-3.3.1) and place it in -
   `gcr.io/mapr-252711/spark-3.3.1-hive-example`

   
2. Create PVCs with the name - `spark-hive-claim`
   and place the file kv1.txt in
   `/opt/spark/work-dir/spark-warehouse/`
   kv1.txt is located in the resource folder
   - `src/main/resources/kv1.txt`

### Create the hivesite config map using the following command

`kubectl apply -f hivesite-cm.yaml`

This sets the metastore thrift uri which the spark job uses

### Run the Spark job using the following command

`kubectl apply -f spark-hive-metastore.yaml`
