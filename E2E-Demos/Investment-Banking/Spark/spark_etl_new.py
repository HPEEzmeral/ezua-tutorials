from pyspark.sql import SparkSession
from pyspark.sql import *
import pyspark.sql.functions as F
from pyspark.sql.functions import *
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')
spark = SparkSession.builder.master("local").appName("ETL").getOrCreate()

df1=spark.read.format('csv').option("header","true").option("inferSchema","true").load(f"file:///mounts/shared-volume/exported_by_airflow/from_minio/bank{today}.csv")

df2=spark.read.format('csv').option("header","true").option("inferSchema","true").load(f"file:///mounts/shared-volume/exported_by_airflow/from_mysql/`bank{today}`.csv")

df1.show()
df2.show()

# Schema of Dataframe 1

df1.printSchema()

#schema of Dataframe 2

df2.printSchema()

# Total Rows of Dataframe 1

df1.count()

# Total Rows of Dataframe 2

df2.count()


# Find duplicate rows in Dataframe 1

duplicate_rows = df1.count() - df1.dropDuplicates().count()
print(duplicate_rows)


# Find duplicate rows in Dataframe 2

duplicate_rows = df2.count() - df2.dropDuplicates().count()
print(duplicate_rows)


# Drop duplicate rows and update the original DataFrame
df2 = df2.dropDuplicates()
df2.count()



# Finding Null values in Dataframe 1

df1.select([count(when(isnan(c),c)).alias(c) for c in df1.columns]).show()



null_counts = df1.agg(*[count(when(col(c).isNull(), c)).alias(c) for c in df1.columns])

# Display the null counts
null_counts.show()

# Finding Null values in Dataframe 2

df2.select([count(when(isnan(c),c)).alias(c) for c in df2.columns]).show()


null_counts = df2.agg(*[count(when(col(c).isNull(), c)).alias(c) for c in df2.columns])

# Display the null counts
null_counts.show()


# Calculate mode of the column
mode = df2.groupBy('default1').agg(count('*').alias('count')).orderBy(col('count').desc()).select(col('default1')).first()[0]

# Fill null values with mode value
df2 = df2.fillna(mode, subset=['default1'])
# Calculate mode of the column
mode = df2.groupBy('loan').agg(count('*').alias('count')).orderBy(col('count').desc()).select(col('loan')).first()[0]

# Fill null values with mode value
df2 = df2.fillna(mode, subset=['loan'])
# Calculate mode of the column
mode = df2.groupBy('poutcome').agg(count('*').alias('count')).orderBy(col('count').desc()).select(col('poutcome')).first()[0]

# Fill null values with mode value
df2 = df2.fillna(mode, subset=['poutcome'])
null_counts = df2.agg(*[count(when(col(c).isNull(), c)).alias(c) for c in df2.columns])

# Display the null counts
null_counts.show()


df1.printSchema()

df2.printSchema()

# concatenate the two dataframes

df = df1.union(df2)
#Total Records after joining both dataframe

df.count()


df.show(50,truncate=False)
df.count()

df.head(25)

df = df.withColumnRenamed("y", "target")

df.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").csv(f"s3a://bank/merged_data{today}")
