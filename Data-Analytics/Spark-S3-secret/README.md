# EZAF Spark Secret Creation

This notebook example provides a way to showcase how to create s3 secret consumed by spark application YAML
and Livy session.

### Run the spark secret creation notebook example

The example will read the environment values and create s3 secret in the current user's namespace.
This secret can be referenced later via 'spark.mapr.extraconf.secret' spark config option:

```
spec:
  sparkConf:
    spark.mapr.extraconf.secret: "<k8s-secret-name>"
```

