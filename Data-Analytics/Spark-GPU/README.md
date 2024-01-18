## Running spark-on-gpu example
###### Configuration in yaml file (do not try to apply it as-is, it has a fake path to the app file)
Note: if not configured properly, spark functions will run on CPU instead of GPU, even if GPU-specific image is used.

Note: do not allocate GPUs for driver pod, it doesn't have any sense. GPUs are used by executors only.

To run spark on GPUs, make sure to:

1. Use 'spark-gpu-...' image. As of Q1 timeframe, we provide this image: gcr.io/mapr-252711/spark-gpu-3.5.0:v3.5.0. 
Depending on the controller, spark image can be set:
   a. Spark operator: via 'image' value in yaml
   b. Livy server: via 'spark.kubernetes.container.image' option in sparkConf.
2. Add the following spark configuration options to enable RAPIDs plugin and allocate GPU for executors. This part of options is spark-version independent.
```yaml
# Enabling RAPIDs plugin
spark.plugins: "com.nvidia.spark.SQLPlugin"
spark.rapids.sql.enabled: "true"
spark.rapids.force.caller.classloader: "false"
 
# GPU allocation and discovery settings
spark.task.resource.gpu.amount: "1"
spark.executor.resource.gpu.amount: "1"
spark.executor.resource.gpu.vendor: "nvidia.com"
```
3. Set path to GPU-discovery script. In spark images, it's built-in at path "/opt/mapr/spark/spark-[VERSION]/examples/src/main/scripts/getGpusResources.sh". Make sure to replace [VERSION] with actual spark version. Example for 3.5.0:
```yaml
spark.executor.resource.gpu.discoveryScript: "/opt/mapr/spark/spark-3.5.0/examples/src/main/scripts/getGpusResources.sh"
```
4. Set RAPIDs shim layer to be used for execution. Spark is compatible with its corresponding open-source spark version. RAPIDs jar includes shim layer provider classes named "com.nvidia.spark.rapids.shims.[spark-identifier].SparkShimServiceProvider", where 'spark-identifier' might be spark350 etc. For spark-3.5.0 identifier is "spark350". So for spark-gpu-3.5.0 image, this setting will be:
```yaml
spark.rapids.shims-provider-override: "com.nvidia.spark.rapids.shims.spark350.SparkShimServiceProvider"
```
5. Run the scala or python example as exampled in their respective README.md files