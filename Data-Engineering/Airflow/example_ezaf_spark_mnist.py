from airflow import DAG
from airflow.models.param import Param
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_active_runs': 1,
    'retries': 0
}

dag = DAG(
    'spark_read_write_parquet_mnist',
    default_args=default_args,
    schedule_interval=None,
    tags=['e2e example', 'ezaf', 'spark', 'parquet', 'mnist'],
    params={
        'username': Param("hpedemo-user01", type="string"),
        'training_path': Param("mnist-spark-data", type="string"),
        's3_secret_name': Param("spark-s3-creds", type="string"),
        'airgap_registry_url': Param("", type="string", pattern="^$|^.+/$")
    }
)

submit = SparkKubernetesOperator(
    task_id='submit',
    namespace="spark",
    application_file="example_ezaf_spark_mnist.yaml",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True
)
