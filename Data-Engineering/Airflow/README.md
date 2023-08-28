# EZAF Airflow Examples

### Airflow DAGs:
* **Financial Time Series example**
  * spark_read_csv_write_parquet_fts
    * reads csv from S3 bucket and writes parquet to target folder (DF)
    * Spark application is placed inside Docker image
* **Mnist example**
  * spark_read_write_parquet_mnist
    * reads **binary** from S3 bucket and writes parquet to target folder (DF)
    * Spark application is placed inside Docker image
