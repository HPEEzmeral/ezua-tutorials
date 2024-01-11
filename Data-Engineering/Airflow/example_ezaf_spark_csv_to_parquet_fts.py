from airflow import DAG
from airflow.models.param import Param
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import (
    SparkKubernetesOperator,
)
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import (
    SparkKubernetesSensor,
)
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "max_active_runs": 1,
    "retries": 0,
}

dag = DAG(
    "spark_read_csv_write_parquet_fts",
    default_args=default_args,
    schedule_interval=None,
    tags=["e2e example", "ezaf", "spark", "csv", "parquet", "fts"],
    params={
        "export_path": Param(
            "financial-processed",
            type="string",
            description="Path to folder on user volume to export processed data for further training",
        ),
        "s3_endpoint": Param(
            "local-s3-service.ezdata-system.svc.cluster.local:30000",
            type="string",
            description="S3 endpoint to pull csv data from",
        ),
        "s3_endpoint_ssl_enabled": Param(
            False, type="boolean", description="Whether to use SSL for S3 endpoint"
        ),
        "s3_bucket": Param(
            "ezaf-demo", type="string", description="S3 bucket to pull csv data from"
        ),
        "s3_path": Param(
            "data/financial.csv",
            type="string",
            description="S3 key to pull csv data from",
        ),
        "airgap_registry_url": Param(
            "",
            type=["null", "string"],
            pattern=r"^$|^\S+/$",
            description="Airgap registry url. Trailing slash in the end is required",
        ),
    },
    render_template_as_native_obj=True,
    access_control={"All": {"can_read", "can_edit", "can_delete"}},
)

submit = SparkKubernetesOperator(
    task_id="submit",
    application_file="example_ezaf_spark_csv_to_parquet_fts.yaml",
    do_xcom_push=True,
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True,
)

sensor = SparkKubernetesSensor(
    task_id="monitor",
    application_name="{{ task_instance.xcom_pull(task_ids='submit')['metadata']['name'] }}",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    attach_log=True,
)

submit >> sensor
