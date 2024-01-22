# EZAF Spark Example

This folder contains Data Transfer Spark example which you can manually submit via Spark operator in your **k8s cluster** .

### Configuration
To setup this example the following steps are requried:

1. Create a bucket named "ezua-demo" in minio.

2. Place the mnist folder to this path `s3a://ezua-demo/data/mnist`.

3. Update the `spark.hadoop.fs.s3a.aws.credentials.provider` and populate with `org.apache.spark.s3a.EzSparkAWSCredentialProvider` in sparkConf.

Note: To access local-s3 from OSS Spark you need to explicitly specify Access Key and Secret Key as OSS Spark can not utilize our implementation of EzSparkAWSCredentialProvider.

To do this you need to add the following configuration to Spark Application:

spark.hadoop.fs.s3a.access.key <ACCESS_KEY>
spark.hadoop.fs.s3a.secret.key <SECRET_KEY>

Alternatively, you can set Access Key and Secret Key as environment variables:

spark.kubernetes.driverEnv.AWS_ACCESS_KEY_ID: <ACCESS_KEY>
spark.kubernetes.driverEnv.AWS_ACCESS_KEY_ID: <SECRET_KEY>
spark.kubernetes.executorEnv.AWS_ACCESS_KEY_ID: <ACCESS_KEY>
spark.kubernetes.executorEnv.AWS_SECRET_ACCESS_KEY: <SECRET_KEY>

However, using this options user wont be able to automatically refresh those tokens from the Secret mounted into Pod.

#### Usage
By default, the workflow consists of these steps:

1. Navigate to the Spark Operator under Analytics in Ezmeral Unified Analytics.

2. Create Application by uploading the `DataTransferMnist.yaml` file.

3. Review the entire yaml for any discrepancy and click on Create Spark Application.

4. Watch the logs for expected output, it would create parquet file at the destination folder in this case `file:///mounts/shared-volume/mnist-spark-data`.
