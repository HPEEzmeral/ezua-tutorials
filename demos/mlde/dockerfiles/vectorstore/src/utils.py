import os
import logging
import boto3
import urllib


logger = logging.getLogger(__name__)

access_key = os.getenv("MINIO_ACCESS_KEY")
secret_key = os.getenv("MINIO_SECRET_KEY")
endpoint_url = os.getenv("MLFLOW_S3_ENDPOINT_URL")


def _get_s3_client():
    return boto3.client(
        service_name="s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url,
        verify=False)


def download_directory(uri: str) -> str:
    """Download the directore in the given URI.

    Args:
        uri (str): The URI of the directory object.
    """
    local_dir = "db"

    client = _get_s3_client()

    parsed_uri = urllib.parse.urlparse(uri)
    bucket_name = parsed_uri.netloc
    s3_folder = parsed_uri.path.lstrip('/')

    paginator = client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_folder):
        for obj in page.get('Contents', []):
            local_file_path = os.path.join(local_dir, obj['Key'][len(s3_folder):].lstrip('/'))
            if not os.path.exists(os.path.dirname(local_file_path)):
                os.makedirs(os.path.dirname(local_file_path))
            client.download_file(bucket_name, obj['Key'], local_file_path)
            print(f"Downloaded {obj['Key']} to {local_file_path}")

    return "db"
