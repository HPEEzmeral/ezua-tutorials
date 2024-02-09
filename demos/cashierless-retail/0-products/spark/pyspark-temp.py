from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("Currency Conversion") \
    .getOrCreate()

# Database connection details
db_url = "jdbc:mysql://localhost:3306/database_name"
db_properties = {
    "user": "username",
    "password": "password",
    "driver": "org.mariadb.jdbc.Driver"
}

# Read the data from the MariaDB table
df = spark.read \
    .format("jdbc") \
    .option("url", db_url) \
    .option("dbtable", "table_name") \
    .option("properties", db_properties) \
    .load()

# Define the conversion rate
conversion_rate = 1.21  # Assuming 1 Euro = 1.21 US dollars

# Perform the currency conversion
df = df.withColumn("TOTALSALES_USD", df["TOTALSALES"] * conversion_rate)

# Show the converted data
df.show()

# Save the converted data to a new table in the database
df.write \
    .format("jdbc") \
    .option("url", db_url) \
    .option("dbtable", "converted_table_name") \
    .option("properties", db_properties) \
    .save()

# Stop the SparkSession
spark.stop()