import os
import logging
import boto3
import urllib
import posixpath


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
    os.environ["HTTPS_PROXY"] = ""
    client = _get_s3_client()

    parsed_uri = urllib.parse.urlparse(uri)
    bucket = parsed_uri.netloc
    prefix = posixpath.dirname(parsed_uri.path)

    try:
        logger.info(f"Fetching the database in bucket {bucket}"
                    f" with key prefix {prefix}.")
        response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if "Contents" in response:
            os.makedirs("db", exist_ok=True)
            os.makedirs("db/index", exist_ok=True)
            objects = response["Contents"]
            for obj in objects:
                # Extract the object key and remove the common prefix
                object_key = obj["Key"]
                file_name = posixpath.basename(object_key)
                logger.info(f"objects: {object_key}")

                if file_name.endswith(".parquet"):
                    # Download the object
                    client.download_file(bucket, object_key, f"db/{file_name}")
                    logger.info(f"Downloaded object: {object_key}")
                else:
                    client.download_file(bucket, object_key, f"db/index/{file_name}")
                    logger.info(f"Downloaded object: {object_key}")

        else:
            logger.info("No objects found in the directory.")
    except Exception as e:
        logger.error(f"Error downloading directory: {e}")

    return "db"
