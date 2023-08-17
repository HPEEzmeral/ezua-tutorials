from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models.param import Param

from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023,7,5),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG(
    'spark-etl-new',
    default_args=default_args,
    description='Banking-data-demo',
    schedule_interval=None,
    tags=['e2e example','ETL', 'spark'],
    params={
        'username': Param("hpedemo-user01", type="string"),
        's3_secret_name': Param("spark-s3-creds", type="string")
    }
)

def start_job():
    print("Start Data Reading from Minio S3 Bucket and QA1 MySQL Database...")

def end_job():
    print("Data Loading to S3 Done...")

task1 = PythonOperator(
    task_id='Start_Data_Reading',
    python_callable=start_job,
    dag=dag,
)

task2=SparkKubernetesOperator(
    task_id='Spark_etl_submit',
    namespace="spark",
    application_file="spark_etl_new.yaml",
    do_xcom_push=True,
    dag=dag,
    api_group="sparkoperator.hpe.com",
    enable_impersonation_from_ldap_user=True
)
task3 = PythonOperator(
    task_id='Data_Loading_Done',
    python_callable=end_job,
    dag=dag,
)
task1>>task2>> task3
