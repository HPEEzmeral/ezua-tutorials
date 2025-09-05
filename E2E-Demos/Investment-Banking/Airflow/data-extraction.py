import os
import shutil
import base64
import time
import jwt
import decimal
import requests
import urllib3
import boto3
from datetime import datetime
from os import path
from airflow import DAG
from airflow.decorators import task
from airflow.models.param import Param
from airflow.utils.dates import days_ago
from airflow.operators.python import get_current_context
from airflow.providers.cncf.kubernetes.hooks.kubernetes import KubernetesHook
import pandas as pd
import botocore.exceptions
from pyhive import presto

def get_token():
    """Fetch auth token from K8s secret."""
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace", "r") as f:
        namespace = f.read()
    k8sCoreApiClient = KubernetesHook().core_v1_client
    secret = k8sCoreApiClient.read_namespaced_secret("access-token", namespace)
    token_encoded = secret.data["AUTH_TOKEN"]  # type: ignore
    return base64.b64decode(token_encoded).decode("utf-8")


def get_s3_client(endpoint_host: str, ssl_enabled: bool):
    """Return boto3 client configured with dynamic JWT auth."""
    endpoint_url = f"http{'s' if ssl_enabled else ''}://{endpoint_host}"
    jwt_token = get_token()
    s3 = boto3.client(
        "s3",
        aws_access_key_id=jwt_token,
        aws_secret_access_key="s3",
        endpoint_url=endpoint_url,
        use_ssl=ssl_enabled,
    )
    return s3


def get_presto_connection(params, jwt_token):
    """Create Presto connection patched with JWT auth headers."""
    decoded_token = jwt.decode(jwt_token, options={"verify_signature": False})
    username_from_token = decoded_token.get("preferred_username", "")

    host = params["presto_host"]
    port = params["presto_port"]
    protocol = params["presto_protocol"]
    catalog = params["presto_catalog"]
    schema = params["presto_schema"]
    user = params["presto_user"] or username_from_token

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    session = requests.Session()
    session.verify = False
    session.headers.update({"Authorization": f"Bearer {jwt_token}"})

    original_post = requests.post
    original_get = requests.get

    def patched_post(*args, **kwargs):
        kwargs["verify"] = False
        kwargs.setdefault("headers", {}).update(session.headers)
        return original_post(*args, **kwargs)

    def patched_get(*args, **kwargs):
        kwargs["verify"] = False
        kwargs.setdefault("headers", {}).update(session.headers)
        return original_get(*args, **kwargs)

    requests.post = patched_post
    requests.get = patched_get

    return presto.connect(
        host=host,
        port=port,
        catalog=catalog,
        schema=schema,
        username=user,
        protocol=protocol,
    )

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

with DAG(
    'data-extraction',
    default_args=default_args,
    schedule_interval=None,
    tags=['DF', 'S3', 'Presto'],
    params={
        # S3 params
        's3_endpoint': Param("minio-service.ezdata-system.svc.cluster.local:30000", type="string"),
        's3_endpoint_ssl_enabled': Param(False, type="boolean"),
        's3_bucket_name': Param("bank", type="string"),
        's3_files_prefix': Param(f"bank.csv", type="string"),
        'result_path_in_shared_volume': Param("exported_by_airflow", type="string"),
        'result_path_prefix_s3': Param("from_minio", type="string"),

        # Presto params
        'presto_host': Param("ezpresto-svc-https-locator.ezpresto.svc.cluster.local", type="string"),
        'presto_port': Param(8081, type="integer"),
        'presto_protocol': Param("https", type="string", enum=["http", "https"]),
        'presto_catalog': Param("mysql", type="string"),
        'presto_schema': Param("bank_demo", type="string"),
        'presto_user': Param("", type=["null", "string"]),
        'presto_tables_list': Param(f"bank", type="string"),
        'result_path_prefix_presto': Param("from_presto", type="string"),
    },
    access_control={'All': {'can_read', 'can_edit', 'can_delete'}}
) as dag:

    @task
    def cleanup_export_dir():
        context = get_current_context()
        global_result_path = context['params']['result_path_in_shared_volume']
        export_path = path.join("/mnt/shared", global_result_path)
        if path.exists(export_path):
            shutil.rmtree(export_path)
            return f"Deleted directory {export_path}"
        return "Nothing to clean"

    @task
    def get_all_filepaths_from_s3_path():
        context = get_current_context()
        bucket_name = context['params']['s3_bucket_name']
        prefix = context['params']['s3_files_prefix']
        s3 = get_s3_client(
            context['params']['s3_endpoint'],
            context['params']['s3_endpoint_ssl_enabled']
        )
        try:
            resp = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            if "Contents" in resp:
                return [obj["Key"] for obj in resp["Contents"]]
            return []
        except botocore.exceptions.ClientError as e:
            raise RuntimeError(f"Error listing S3 objects: {str(e)}")

    @task
    def download_s3_file_to_shared_volume(filepath):
        context = get_current_context()
        bucket_name = context['params']['s3_bucket_name']
        global_result_path = context['params']['result_path_in_shared_volume']
        s3_prefix_path = context['params']['result_path_prefix_s3']
        s3 = get_s3_client(
            context['params']['s3_endpoint'],
            context['params']['s3_endpoint_ssl_enabled']
        )

        subdir_in_s3 = path.dirname(filepath)
        local_dir = path.join("/mnt/shared", global_result_path, s3_prefix_path, subdir_in_s3)
        os.makedirs(local_dir, mode=0o777, exist_ok=True)

        local_file_path = path.join(local_dir, path.basename(filepath))
        try:
            s3.download_file(bucket_name, filepath, local_file_path)
            os.chmod(local_file_path, 0o777)
            return local_file_path
        except botocore.exceptions.ClientError as e:
            raise RuntimeError(f"Error downloading {filepath} from S3: {str(e)}")

    @task
    def split_presto_tables_from_str():
        context = get_current_context()
        presto_tables_list = context['params']['presto_tables_list']
        return presto_tables_list.split(',')

    @task
    def export_presto_table_to_csv_shared_volume(table):
        context = get_current_context()
        global_result_path = context['params']['result_path_in_shared_volume']
        presto_prefix_path = context['params']['result_path_prefix_presto']
        table_filename = f"{table}.csv"
        base_csv_path = path.join("/mnt/shared", global_result_path, presto_prefix_path)
        csv_path_real = path.join(base_csv_path, table_filename)
        os.umask(0o000)
        os.makedirs(base_csv_path, mode=0o777, exist_ok=True)

        jwt_token = get_token()
        conn = get_presto_connection(context['params'], jwt_token)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        result = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(result, columns=colnames)
        df.to_csv(csv_path_real, index=False)
        os.chmod(csv_path_real, 0o777)
        return csv_path_real

    cleanup_export_dir_task = cleanup_export_dir()
    cleanup_export_dir_task >> download_s3_file_to_shared_volume.expand(filepath=get_all_filepaths_from_s3_path())
    cleanup_export_dir_task >> export_presto_table_to_csv_shared_volume.expand(table=split_presto_tables_from_str())

