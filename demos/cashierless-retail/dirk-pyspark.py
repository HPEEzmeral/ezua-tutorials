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
      .option("url", "jdbc:presto://ezpresto.ezua12.ezmeral.demo.local:443") \
      .option("user", "demo-user") \
      .option("password", "Hpepoc@123") \
      .option("SSL", "true") \
      .option("IgnoreSSLChecks", "true") \
      .option("query", "SELECT * FROM ctc_mysql.discover.czech UNION ALL SELECT * FROM ctc_mysql.discover.germany UNION ALL ( SELECT PRODUCTID , PRODUCT , TYPE , UNITPRICE , UNIT , QTY , TOTALSALES , CURRENCY , STORE , (CASE WHEN (country = 'Swiss') THEN 'Switzerland' ELSE country END) COUNTRY , YEAR FROM ctc_mysql.discover.swiss )") \
      .load() 
    df.show()


