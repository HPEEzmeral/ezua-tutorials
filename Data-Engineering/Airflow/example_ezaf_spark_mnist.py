from airflow import DAG
from airflow.models.param import Param
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
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
        'training_path': Param("mnist-spark-data", type="string"),
        's3_secret_name': Param("spark-s3-creds", type="string"),
        'airgap_registry_url': Param("", type=["null", "string"], pattern=r"^$|^\S+/$")
    },
    render_template_as_native_obj=True,
    access_control={
        'All': {
            'can_read',
            'can_edit',
            'can_delete'
        }
    }
)

submit = SparkKubernetesOperator(
    task_id='submit',
    application_file="example_ezaf_spark_mnist.yaml",
    do_xcom_push=True,
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True
)

sensor = SparkKubernetesSensor(
    task_id='monitor',
    application_name="{{ task_instance.xcom_pull(task_ids='submit')['metadata']['name'] }}",
    dag=dag,
    api_group="sparkoperator.hpe.com",
    attach_log=True
)

submit >> sensor
