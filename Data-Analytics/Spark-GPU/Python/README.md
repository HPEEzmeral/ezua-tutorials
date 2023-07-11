###### This example shows how to configure a spark application to allocate and utilize GPU in sql computations for Pyspark
1. Put the py file to available location, e.g., maprfs
2. Run the python-gpu example

To test the same on livy, use the following code:
```python
sqlContext = SQLContext(sc)
 
df = sqlContext.createDataFrame([1,2,3], "int").toDF("value")
df.createOrReplaceTempView("df")
 
sqlContext.sql("SELECT * FROM df WHERE value<>1").explain()
sqlContext.sql("SELECT * FROM df WHERE value<>1").show()
```

The expected output of 'explain' should look like this:
```shell
== Physical Plan ==
GpuColumnarToRow false
+- GpuFilter NOT (value#2 = 1), true
   +- GpuRowToColumnar targetsize(2147483647)
      +- *(1) SerializeFromObject [input[0, int, false] AS value#2]
         +- Scan[obj#1]
```
For comparison, if GPU acceleration is not enabled, output will be:
```shell
== Physical Plan ==
*(1) Filter NOT (value#2 = 1)
+- *(1) SerializeFromObject [input[0, int, false] AS value#2]
   +- Scan[obj#1]
```
