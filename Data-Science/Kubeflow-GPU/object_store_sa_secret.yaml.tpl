apiVersion: v1
kind: Secret
metadata:
  name: gpu-mnist-minio-secret
  annotations:
     serving.kserve.io/s3-endpoint: "local-s3-service.ezdata-system.svc.cluster.local:30000/"
     serving.kserve.io/s3-usehttps: "0"
     serving.kserve.io/s3-verifyssl: "0"
     serving.kserve.io/s3-useanoncredential: "false"
     serving.kserve.io/s3-cabundle: ""
type: Opaque
stringData:
  AWS_ACCESS_KEY_ID: "$AUTH_TOKEN"
  AWS_SECRET_ACCESS_KEY: "$AUTH_TOKEN"
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: gpu-mnist-minio-sa
secrets:
- name: gpu-mnist-minio-secret
