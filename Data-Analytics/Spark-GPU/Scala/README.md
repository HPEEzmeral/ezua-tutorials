###### This example shows how to configure a spark application to allocate and utilize GPU in sql computations for Scala 
Examples for Ezmeral Spark on Kubernetes v3.3.1
Compatible with ECP v5.4.0

Directories structure:
- apps - custom applications source code. Includes sources of example applications that are not included to spark
  distribution
- crs - SparkApplication yaml files

1. Build SparkDemo.jar file as described:
  Building examples jar:
```shell
cd apps
mvn clean package
```

2. Put the jar file to available location, e.g., maprfs
3. Run the scala-gpu example, check physical plan in the output logs:
```shell
== Physical Plan ==
GpuColumnarToRow false
+- GpuFilter NOT (value#2 = 1), true
   +- GpuRowToColumnar targetsize(2147483647)
      +- *(1) SerializeFromObject [input[0, int, false] AS value#2]
         +- Scan[obj#1]
```
4. Disable RAPIDs sql feature by changing the following option in yaml file:
```yaml
spark.conf:
  ...
  spark.rapids.sql.enabled: "false"
  ...
```
5. Restart application and check the physical plan again. Since sql-on-gpu is disabled, now it should look like this:
```shell
== Physical Plan ==
*(1) Filter NOT (value#2 = 1)
+- *(1) SerializeFromObject [input[0, int, false] AS value#2]
   +- Scan[obj#1]
```


