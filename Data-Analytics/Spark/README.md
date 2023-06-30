# EZAF Spark Example

This is a Spark ETL example which you can manually submit via Spark operator in your **k8s cluster** .
Deployed Spark app reads the raw data from **S3 Object Store**, preprocesses it in distributed mode and
writes to the **[HPE Data Fabric](https://www.hpe.com/us/en/software/ezmeral-data-fabric.html).**
Processed data will be stored to **PV**, referenced by **PVC**. With that,
you can access it from other EZAF components by plugging the same **PVC**

### Configuration

To configure Spark example, we use [Embed .jar file into the **docker image**](k8s/DataProcessTransferFts-JarLocal-3.3.1.yaml)
of delivering app's **.jar** file.

> **Note:** For more detailed acquaintance with Spark config you can look through following table with more extended explanation

<details>
<summary><code>Spark Config</code></summary>

| Parameter               | Description                                                                                            | Example Value                                                                                                                                                                                                                                                                                                                                          |
|-------------------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `*.image`               | Image that is used to run Spark itself                                                                 | <ul><li>`gcr.io/mapr-252711/spark-demo-example:v1.0`</li>Custom image with `.jar` file embedded<br/><br/><li>`gcr.io/mapr-252711/spark-3.3.1:202301161621R`</li>Pure Spark image<ul>                                                                                                                                                                   |
 | `*.mainApplicationFile` | Path inside the pod that is used by spark to find `.jar` file with app                                 | <ul><li>`local:///tmp/DataProcessTransfer.jar`</li>Path in which `.jar` file was embedded into image<br/><br/><li>`local///mounts/data/DataProcessTransfer.jar`</li>:warning: The specified path must be mounted to the `PV`<br/><br/><li>`maprfs:///home/spark/DataProcessTransfer.jar`</li>Path in which `.jar` file can be reached im `MaprFS`</ul> |
 | `*.mainClass`           | The fully qualified name of the class that contains the main method for the Java and Scala application | `com.mapr.sparkdemo.DataTransferDemo`                                                                                                                                                                                                                                                                                                                  |
 | `*.arguments`           | Arguments passed to the main method of your main class (_i.e._ command arguments)                      | <ul><li>`s3a://ezaf-demo/data/financial-partitioned`</li>Data source path<br/><br/><li>`parquet`</li>Data source format<br/><br/><li>`file:///mounts/data/financial-processed`<br/>Data destination path. :warning: The specified path must be mounted to `PV`</li><br/><li>`parquet`</li>Data destination format</ul>                                 | 
 | `*.mountPath`           | Path inside the Pod that would be mounted to persistent storage                                        | `/mounts/data`                                                                                                                                                                                                                                                                                                                                         |
 | `*.claimName`           | PVC's name that claims to persistent volume, that spark will write data to                             | `<username>-<namespace>-pvc`<br/>e.g. `john-doe-spark-pvc`                                                                                                                                                                                                                                                                                             |
 | `*.namespace`           | Namespace where k8s Custom Resource HPE HCP Tenant is present                                          | `spark`                                                                                                                                                                                                                                                                                                                                                | 

</details>

### Installation

Spark App can be deployed via [installation script][1].

#### Usage

```bash
/bin/bash devops/install.sh
```

By default, its workflow consists of 4 steps:

1. Gets [.jar][2] file, based on [scala code](src/DataProcessTransfer/DataProcessTransfer.scala)

2. Inserts the [.jar][2] file to the custom [image](dockerfiles/SparkJarLocal-3.3.1.Dockerfile).

3. Pushes built image to the repo, specified in [script][1]

4. Deploys your Spark app as the LDAP user, specified in [script][1]


### Troubleshooting

1. You cannot submit your app due to such an error:
`Please verify the user is in LDAP and has rights to use the Tenant` on the applying yaml step
   * Tip: run `kubectl -n [namespace] describe rolebindings.rbac.authorization.k8s.io hpe-[namespace]-user` 
    and verify that user (or user group) is in the subject list.
2. Your application fails with such an error: 
`ERROR FileOutputCommitter: Mkdirs failed to create [SomePath]`
    * Tip: Make sure destination path is available for writing within the context of Linux file permissions in `maprfs`


[1]:devops/install.sh
[2]:src/DataProcessTransfer/DataProcessTransfer.jar
