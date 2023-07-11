from pyspark.sql import SQLContext
from pyspark import SparkConf
from pyspark import SparkContext
 
conf = SparkConf()
sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)
 
df = sqlContext.createDataFrame([1,2,3], "int").toDF("value")
df.createOrReplaceTempView("df")
 
sqlContext.sql("SELECT * FROM df WHERE value<>1").explain()
sqlContext.sql("SELECT * FROM df WHERE value<>1").show()
 
sc.stop()