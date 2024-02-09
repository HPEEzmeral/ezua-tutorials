from pyspark.sql import SparkSession

if __name__ == "__main__":
    print("pyspark session started..")
    spark = SparkSession.builder \
        .appName("discoverdemo") \
        .getOrCreate()
    
    sc = spark.sparkContext
    
    df = spark.read \
      .format("jdbc") \
      .option("driver", "com.facebook.presto.jdbc.PrestoDriver") \
      .option("url", "jdbc:presto://ezpresto.hpe-discover-23-ezaf.com:443") \
      .option("user", "discover-user01") \
      .option("password", "Hpepoc@123") \
      .option("SSL", "true") \
      .option("IgnoreSSLChecks", "true") \
      .option("query", "SELECT product , sum(qty) total_quantity_sold FROM ( SELECT product , qty FROM czech_mysql.discover.czech UNION ALL SELECT product , qty FROM german_mariadb.discover.germany UNION ALL SELECT product , qty FROM swiss_mysql.discover.swiss ) combined_sales GROUP BY product ORDER BY total_quantity_sold DESC LIMIT 1") \
      .load() 
    df.show()
