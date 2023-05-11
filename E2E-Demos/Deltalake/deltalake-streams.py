#!/usr/bin/env python

# **Setup and configuration**
from time import sleep
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr
from delta.tables import DeltaTable
import shutil

from pyspark.sql.functions import * 

spark = SparkSession.builder.appName("delta_lake_demo") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")  \
    .getOrCreate()

spark.sparkContext.setLogLevel('ERROR')

BUCKET = "s3a://ezaf-demo"
DATAFILE = BUCKET + "/data/deltalake/"
DEMOFILES = BUCKET + "/data/deltalake/demo"

parquet_path = DEMOFILES + "/loans-paraquet"

spark.read.format("parquet").load(DATAFILE) \
  .write.format("parquet").save(parquet_path)

print("Created a Parquet table at " + parquet_path)

# Create a view on the table called loans_parquet
spark.read.format("parquet").load(parquet_path).createOrReplaceTempView("loans_parquet")
print("Defined view 'loans_parquet'")

# ##### Let's explore this parquet table.
# *Schema of the table*
# - load_id - unique id for each loan
# - funded_amnt - principal amount of the loan funded to the loanee
# - paid_amnt - amount from the principle that has been paid back (ignoring interests)
# - addr_state - state where this loan was funded

spark.sql("select * from loans_parquet").show()

spark.sql("select count(*) from loans_parquet").show()

# **Let's start appending some new data to it using Structured Streaming.**
# 
# - We will generate a stream of data from with randomly generated loan ids and amounts. 
# - In addition, we are going to define a few more useful utility functions.


import random
from pyspark.sql.functions import *
from pyspark.sql.types import *

def random_checkpoint_dir(): 
    return "{}/chkpt/{}".format(DEMOFILES,str(random.randint(0, 10000)))

# User-defined function to generate random state

states = ["CA", "TX", "NY", "IA"]

@udf(returnType=StringType())
def random_state():
    return str(random.choice(states))

# Function to start a streaming query with a stream of randomly generated load data and append to the parquet table
def generate_and_append_data_stream(table_format, table_path):
  
    stream_data = spark.readStream.format("rate").option("rowsPerSecond", 5).load() \
                .withColumn("loan_id", 10000 + col("value")) \
                .withColumn("funded_amnt", (rand() * 5000 + 5000).cast("integer")) \
                .withColumn("paid_amnt", col("funded_amnt") - (rand() * 2000)) \
                .withColumn("addr_state", random_state())
    query = stream_data.writeStream.format(table_format) \
                .option("checkpointLocation", random_checkpoint_dir()) \
                .trigger(processingTime = "10 seconds") \
                .start(table_path)
    return query

# Function to stop all streaming queries 
import os
def stop_all_streams():
    # Stop all the streams
    print("Stopping all streams")
    for s in spark.streams.active:
        s.stop()
    print("Stopped all streams")
#     print("Deleting checkpoints")  
#     try:
#         deleteS3Folder("delta","loans-demo/chkpt")
#     except S3Error as err:
#         print(str(err))
#     print("Deleted checkpoints")

# Let's start a new stream to append data to the Parquet table
stream_query = generate_and_append_data_stream(
    table_format = "parquet", 
    table_path = parquet_path)
sleep(30)

# Let's see if the data is being added to the table or not
spark.read.format("parquet").load(parquet_path).count()

# Where did our existing 14705 rows go? Let's see the data once again
spark.read.format("parquet").load(parquet_path).show()

# **Where did the two new columns `timestamp` and `value` come from? What happened here!**
# 
# What really happened is that when the streaming query started adding new data to the Parquet table, it did not properly account for the existing data in the table. Furthermore, the new data files that written out accidentally had two extra columns in the schema. Hence, when reading the table, the 2 different schema from different files were merged together, thus unexpectedly modifying the schema of the table.
stop_all_streams()

print("2. Batch + stream processing and schema enforcement with Delta Lake")
# ## Let's understand Delta Lake solves these particular problems (among many others). We will start by creating a Delta table from the original data.
# 

# Configure Delta Lake Silver Path
delta_path = DEMOFILES + "/loans-delta"

spark.sql("set spark.sql.shuffle.partitions = 1")
spark.sql("set spark.databricks.delta.snapshotPartitions = 1")

# Create the Delta table with the same loans data
spark.read.format("parquet").load(DATAFILE).write.format("delta").save(delta_path)
print("Created a Delta table at " + delta_path)

spark.read.format("delta").load(delta_path).createOrReplaceTempView("loans_delta")
print("Defined view 'loans_delta'")

spark.sql("select count(*) from loans_delta").show()

spark.sql("select * from loans_delta").show()

# Let's run a streaming count(*) on the table so that the count updates automatically
spark.readStream.format("delta").load(delta_path).createOrReplaceTempView("loans_delta_stream")
spark.sql("select count(*) from loans_delta_stream")

# Now let's try writing the streaming appends once again
stream_query_2 = generate_and_append_data_stream(table_format = "delta", table_path = delta_path)


# The writes were blocked because the schema of the new data did not match the schema of table
# **Now, let's fix the streaming query by selecting the columns we want to write.**

from pyspark.sql.functions import *
# Generate a stream of randomly generated load data and append to the parquet table
def generate_and_append_data_stream_fixed(table_format, table_path):
    
    stream_data = spark.readStream.format("rate").option("rowsPerSecond", 50).load() \
            .withColumn("loan_id", 10000 + col("value")) \
            .withColumn("funded_amnt", (rand() * 5000 + 5000).cast("integer")) \
            .withColumn("paid_amnt", col("funded_amnt") - (rand() * 2000)) \
            .withColumn("addr_state", random_state()) \
            .select("loan_id", "funded_amnt", "paid_amnt", "addr_state")   # *********** FIXED THE SCHEMA OF THE GENERATED DATA *************

    query = stream_data.writeStream.format(table_format) \
            .option("checkpointLocation", random_checkpoint_dir()) \
            .trigger(processingTime="10 seconds") \
            .start(table_path)

    return query

# Now we can successfully write to the table. Note the count in the above streaming query increasing as we write to this table.

stream_query_2 = generate_and_append_data_stream_fixed(table_format = "delta", table_path = delta_path)
sleep(30)

# In fact, we can run multiple concurrent streams writing to that table, it will work together.
stream_query_3 = generate_and_append_data_stream_fixed(table_format = "delta", table_path = delta_path)

sleep(30)

# Just for sanity check, let's query as a batch
spark.sql("select count(*) from loans_delta").show()

stop_all_streams()

# ## Schema Evolution
# - Let's evolve the schema of the table
# - We will run a batch query that will
# - Append some new loans
# - Add a boolean column 'closed' that signifies whether the loan has been closed and paid off or not.
# - We are going to set the option `mergeSchema` to `true` to force the evolution of the Delta table's schema.
# 


cols = ['loan_id', 'funded_amnt', 'paid_amnt', 'addr_state', 'closed']

items = [
  (1111111, 1000, 1000.0, 'TX', True), 
  (2222222, 2000, 0.0, 'CA', False)
]

loan_updates = spark.createDataFrame(items, cols) \
.withColumn("funded_amnt", col("funded_amnt").cast("int"))
  
loan_updates.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save(delta_path)

spark.read.format("delta").load(delta_path).show()

print("3. Delete from Delta Lake table")

# Let's see the number of fully paid loans.
spark.sql("SELECT COUNT(*) FROM loans_delta WHERE funded_amnt = paid_amnt").show()

from delta.tables import *

deltaTable = DeltaTable.forPath(spark, delta_path)
deltaTable.delete("funded_amnt = paid_amnt")

# Let's check the number of fully paid loans once again.
spark.sql("SELECT COUNT(*) FROM loans_delta WHERE funded_amnt = paid_amnt").show()

print("4. Audit Delta Lake Table History")
# All changes to the Delta table are recorded as commits in the table's transaction log. As you write into a Delta table or directory, every operation is automatically versioned. You can use the HISTORY command to view the table's history. For more information, check out the [docs](https://docs.delta.io/latest/delta-utility.html#history).

deltaTable = DeltaTable.forPath(spark, delta_path)
deltaTable.history().show()

print("5. Travel back in time")
# - Delta Lake’s time travel feature allows you to access previous versions of the table. Here are some possible uses of this feature:
#     - Auditing Data Changes
#     - Reproducing experiments & reports
#     - Rollbacks
# 
# You can query by using either a timestamp or a version number using Python, Scala, and/or SQL syntax. For this examples we will query a specific version using the Python syntax.

# Let's query the table's state before we deleted the data, which still contains the fully paid loans.
previousVersion = deltaTable.history(1).select("version").collect()[0][0] - 1

spark.read.format("delta") \
    .option("versionAsOf", previousVersion) \
    .load(delta_path) \
    .createOrReplaceTempView("loans_delta_pre_delete")

# We see the same number of fully paid loans that we had seen before delete.
spark.sql("SELECT COUNT(*) FROM loans_delta_pre_delete WHERE funded_amnt = paid_amnt").show()

print("6.  Vacuum old versions of Delta Lake tables")
# 
# While it's nice to be able to time travel to any previous version, sometimes you want actually delete the data from storage completely for reducing storage costs or for compliance reasons (example, GDPR).
# 
# The Vacuum operation deletes data files that have been removed from the table for a certain amount of time. For more information, check out the [docs](https://docs.delta.io/latest/delta-utility.html#vacuum).
# 
# By default, `vacuum()` retains all the data needed for the last 7 days. For this example, since this table does not have 7 days worth of history, we will retain 0 hours, which means to only keep the latest state of the table.


spark.sql("SET spark.databricks.delta.retentionDurationCheck.enabled = false")
deltaTable.vacuum(retentionHours = 0)

print(f"previousversion:{previousVersion}")

spark.read.format("delta").option("versionAsOf", previousVersion).load(delta_path).createOrReplaceTempView("loans_delta_pre_delete")


# Same query as before, but it now fails
try:
    spark.sql("SELECT COUNT(*) FROM loans_delta_pre_delete WHERE funded_amnt = paid_amnt").show()
except Exception as e:
    print(str(e))

print("7. Upsert into Delta Lake table using Merge")
# 
# You can upsert data from an Apache Spark DataFrame into a Delta Lake table using the merge operation. This operation is similar to the SQL MERGE command but has additional support for deletes and extra conditions in updates, inserts, and deletes. For more information checkout the [docs](https://docs.delta.io/latest/delta-update.html#upsert-into-a-table-using-merge).

# With a legacy data pipeline, to insert or update a table, you must:
# 1. Identify the new rows to be inserted
# 2. Identify the rows that will be replaced (i.e. updated)
# 3. Identify all of the rows that are not impacted by the insert or update
# 4. Create a new temp based on all three insert statements
# 5. Delete the original table (and all of those associated files)
# 6. "Rename" the temp table back to the original table name
# 7. Drop the temp table

# Configure Delta Lake Silver Path
delta_small_path = DEMOFILES + "/loans-delta-small"

# Create the Delta table with the same loans data
spark.read.format("parquet").load(DATAFILE) \
    .where("loan_id < 3") \
    .write.format("delta").save(delta_small_path)
print("Created a Delta table at " + delta_small_path)

spark.read.format("delta").load(delta_small_path).createOrReplaceTempView("loans_delta_small")
print("Defined view 'loans_delta_small'")

# Let's focus only on a part of the loans_delta table
spark.sql("select * from loans_delta_small order by loan_id").show()


# **Now, let's say we got some new loan information**
# 1. Existing loan_id = 2 has been fully repaid. The corresponding row needs to be updated.
# 2. New loan_id = 3 has been funded in CA. This is need to be inserted as a new row.


cols = ['loan_id', 'funded_amnt', 'paid_amnt', 'addr_state']
items = [
  (2, 1000, 1000.0, 'TX'), # existing loan's paid_amnt updated, loan paid in full
  (3, 2000, 0.0, 'CA')     # new loan's details
]

loan_updates = spark.createDataFrame(items, cols)

loan_updates.show()


# **Merge can upsert this in a single atomic operation.** 
#  
# SQL `MERGE` command can do both `UPDATE` and `INSERT`.
# ``` 
# MERGE INTO target t
# USING source s
# WHEN MATCHED THEN UPDATE SET ...
# WHEN NOT MATCHED THEN INSERT ....
# ```


from delta.tables import *

delta_table = DeltaTable.forPath(spark, delta_small_path)

delta_table.alias("t").merge(
    loan_updates.alias("s"), 
    "s.loan_id = t.loan_id") \
  .whenMatchedUpdateAll() \
  .whenNotMatchedInsertAll() \
  .execute()

spark.sql("select * from loans_delta_small order by loan_id").show()


# **Note the changes in the table**
# - Existing loan_id = 2 should have been updated with paid_amnt set to 1000. 
# - New loan_id = 3 have been inserted.

print("8. Advanced uses of Merge")

print("8.1 Streaming upserts into a Delta Lake table using merge and foreachBatch")
# 
# You can continuously upsert from a streaming query output using merge inside `foreachBatch` operation of Structured Streaming.
# 
# Let's say, we want to maintain a count of the loans per state in a table, and new loans arrive, we want to update the counts.
# 
# To do this, we will first initialize the table and a few associated UDFs and configurations.

# Generate a stream of randomly generated load data and append to the parquet table
import random
from delta.tables import *
from pyspark.sql.functions import * 
from pyspark.sql.types import *

loan_counts_by_states_path = DEMOFILES + "/loans-by-states"
chkpt_path = "{}/chkpt/{}".format(DEMOFILES, str(random.randint(0, 10000)))


# Initialize the table
spark.createDataFrame([ ('CA', '0') ], ["addr_state" , "count"]).write.format("delta").mode("overwrite").save(loan_counts_by_states_path)


# User-defined function to generate random state
states = ["CA", "TX", "NY", "IA"]
@udf(returnType=StringType())
def random_state():
    return str(random.choice(states))

# Define the function to be called on the output of each micro-batch. 
# This function will use merge to upsert into the Delta table.

loan_counts_by_states_table = DeltaTable.forPath(spark, loan_counts_by_states_path)

# Function to upsert per-state counts generated in each microbatch of a streaming query
# - updated_counts_df = the updated counts generated from a microbatch
def upsert_state_counts_into_delta_table(updated_counts_df, batch_id):
    loan_counts_by_states_table.alias("t").merge(
      updated_counts_df.alias("s"), 
      "s.addr_state = t.addr_state") \
    .whenMatchedUpdateAll() \
    .whenNotMatchedInsertAll() \
    .execute()

# Define and run the streaming query using this function with `foreachBatch`.
# loan_ids that have been complete paid off, random generated
loans_update_stream_data = spark.readStream.format("rate").option("rowsPerSecond", 5).load() \
        .withColumn("loan_id", rand() * 100) \
        .withColumn("funded_amnt", (rand() * 5000 + 5000).cast("integer")) \
        .withColumn("paid_amnt", col("funded_amnt") - (rand() * 2000)) \
        .withColumn("addr_state", random_state()) \
        .createOrReplaceTempView("generated_loads")

# use foreachBatch to define what to do with each output micro-batch DataFrame
query = spark.sql("select addr_state, count(*) as count from generated_loads group by addr_state") \
      .writeStream.format("delta").foreachBatch(upsert_state_counts_into_delta_table) \
      .option("checkpointLocation", chkpt_path) \
      .trigger(processingTime = '3 seconds') \
      .outputMode("update") \
      .start(loan_counts_by_states_path)

sleep(30)
# Let's query the state to see the counts. If you run the following cell repeatedly, 
# you will see that the counts will keep growing.

spark.read.format("delta").load(loan_counts_by_states_path).orderBy("addr_state").show()

stop_all_streams()

print("8.2 Deduplication using `insert-only` merge")

from delta.tables import *

delta_path = DEMOFILES + "/loans-delta2"

# Define new loans table data
data = [
  (0, 1000, 1000.0, 'TX'), 
  (1, 2000, 0.0, 'CA')
]
cols = ['loan_id', 'funded_amnt', 'paid_amnt', 'addr_state']

# Write a new Delta Lake table with the loans data
spark.createDataFrame(data, cols).write.format("delta").save(delta_path)


# Define DeltaTable object
dt = DeltaTable.forPath(spark, delta_path)
dt.toDF().show()

# Define a DataFrame containing new data, some of which is already present in the table
new_data = [  
  (1, 2000, 0.0, 'CA'),    # duplicate, loan_id = 1 is already present in table and don't want to update
  (2, 5000, 1010.0, 'NY')  # new data, not present in table
]
new_data_df = spark.createDataFrame(new_data, cols)

new_data_df.show()

# Run "insert-only" merqe query (i.e., no update clause)
dt = DeltaTable.forPath(spark, delta_path)

dt.alias("t").merge(
    new_data_df.alias("s"), 
    "s.loan_id = t.loan_id") \
  .whenNotMatchedInsertAll() \
  .execute()

dt.toDF().show()

print("""
9. Tutorial Summary
# #### Full support for batch and streaming workloads
# * Delta Lake allows batch and streaming workloads to concurrently read and write to Delta Lake tables with full ACID transactional guarantees.
# #### Schema enforcement and schema evolution
# * Delta Lake provides the ability to specify your schema and enforce it. This helps ensure that the data types are correct and required columns are present, preventing bad data from causing data corruption.
# #### Table History and Time Travel
# * Delta Lake transaction log records details about every change made to data providing a full audit trail of the changes. 
# * You can query previous snapshots of data enabling developers to access and revert to earlier versions of data for audits, rollbacks or to reproduce experiments.
# #### Delete data and Vacuum old versions
# * Delete data from tables using a predicate.
# * Fully remove data from previous versions using Vaccum to save storage and satisfy compliance requirements.
# #### Upsert data using Merge
# * Upsert data into tables from batch and streaming workloads
# * Use extended merge syntax for advanced usecases like data deduplication, change data capture, SCD type 2 operations, etc.
# """)
spark.stop()