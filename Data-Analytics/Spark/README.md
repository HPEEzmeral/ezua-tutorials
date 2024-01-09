# EZAF Spark Example

This folder contains Spark examples which you can manually submit via Spark operator in your **k8s cluster** .

### Configuration


> **Note:** For more detailed acquaintance with Spark config you can look through following table with more extended explanation

<details>
<summary><code>Spark Config</code></summary>

| Parameter               | Description                                                                                            | Example Value                                                                                                                                                                                                                                                                                                                                          |
|-------------------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `*.image`               | Image that is used to run Spark itself                                                                 | <ul><li>`gcr.io/mapr-252711/spark-3.5.0:v3.5.0`</li>Pure Spark image<ul>                                                                                                                                                              |
 | `*.mainApplicationFile` | Path inside the pod that is used by spark to find `executable` file with app                                 | <ul><li>`local:///tmp/<Application>.jar`</li>Path in which `.jar` file was embedded into image<br/><br/><li>`local///mounts/<Application>.jar`</li>:warning: The specified path must be mounted to the `PV`<br/><br/><li>`maprfs:///home/spark/<Application>.jar`</li>Path in which `.jar` file can be reached im `MaprFS`</ul> |
 | `*.mainClass`           | The fully qualified name of the class that contains the main method for the Java and Scala application | `com.mapr.sparkdemo.DataTransferDemo`                                                                                                                                                                                                                                                                                                                  |
 | `*.arguments`           | Arguments passed to the main method of your main class (_i.e._ command arguments)                      | <ul><li>`s3a://ezaf-demo/data/financial.csv`</li>Data source path<br/><br/><li>`csv`</li>Data source format<br/><br/><li>`file:///mounts/data/financial-processed`<br/>Data destination path. :warning: The specified path must be mounted to `PV`</li><br/><li>`parquet`</li>Data destination format</ul>                                             | 
 | `*.mountPath`           | Path inside the Pod that would be mounted to persistent storage                                        | `/mounts/data`                                                                                                                                                                                                                                                                                                                                         |
 | `*.claimName`           | PVC's name that claims to persistent volume, that spark will write data to                             | `<username>-<namespace>-pvc`<br/>e.g. `john-doe-spark-pvc`                                                                                                                                                                                                                                                                                             |
 | `*.namespace`           | Namespace where k8s Custom Resource HPE HCP Tenant is present                                          | `spark`                                                                                                                                                                                                                                                                                                                                                | 

</details>


#### Usage
By default, the workflow consists of these steps:

1. You create a SparkApplication object in k8s by applying the object manifest in yaml file

2. Autotix webhook intercepts ‘create sparkapp’ request, mutates and validates it

3. Mutated and validated object is stored within k8s etcd

4. Spark operator finds new object in etcd and starts processing: it parses the object and creates a ‘spark submitter’ job.

5. Submitter job performs actual ‘spark-submit’ call, which in turn creates driver pod

6. Spark operator internal pod webhook intercepts the driver pod creation and applies pod mutations if needed (e.g., it mounts secrets and PVCs). Mutated pod spec is stored within etcd

7. Pod controller creates driver pod

8. Same happens with executors
