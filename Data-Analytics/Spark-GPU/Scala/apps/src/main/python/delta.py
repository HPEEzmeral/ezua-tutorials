import sys
from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Test Python Delta Lake App") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    data = spark.range(0, 5)
    data.write.format("delta").mode("append").save(sys.argv[1])

    df = spark.read.format("delta").load(sys.argv[1])
    df.show()

    spark.stop()
