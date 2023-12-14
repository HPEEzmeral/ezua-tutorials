apiVersion: v1
kind: Secret
metadata:
  name: spark-s3-creds
type: Opaque
stringData:
  spark-defaults.conf: |
    spark.hadoop.fs.s3a.endpoint local-s3-service.ezdata-system.svc.cluster.local:30000/
    spark.hadoop.fs.s3a.access.key $AUTH_TOKEN
    spark.hadoop.fs.s3a.secret.key $AUTH_TOKEN
