# EZAF Spark Secret Creation

This notebook example provides a way to showcase how to create s3 secret consumed by spark application YAML.

### Run the spark secret creation notebook example

The example will read the environment values and create s3 secret in the current user's namespace.
We should reference this secret in spark application YAML as follows:

```
spec:
  sparkConf:
    spark.mapr.extraconf.secret: "<k8s-secret-name>"
```

