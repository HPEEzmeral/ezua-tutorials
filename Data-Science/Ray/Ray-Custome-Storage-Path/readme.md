## Simple instructions to run experiments.

## EXAMPLE-1
With defined internal_s3_storage path
To complete the tutorial follow simple steps below:
1. Login to you EzAF cluster.
2. Create a new notebook server using the `jupyter-data-science` image.
3. Clone the repository locally.
4. Launch the `run.ipynb` notebook file.
5. Change the filename in entrypoint="python filename" with the file which you need to run.
5. Launch the `internal_s3_storage.py` python script, update the s3_access_key value with fresh AUTH_TOKEN value.
6. This example will executes a log on top of RAY cluster.

## EXAMPLE-2
With defined custom storage path
To complete the tutorial follow simple steps below:
1. Login to you EzAF cluster.
2. Create a new notebook server using the `jupyter-data-science` image.
3. Clone the repository locally.
4. Launch the `run.ipynb` notebook file.
5. Change the filename in entrypoint="python filename" with the filename which you need to run.
6. This example will executes a log on top of RAY cluster.
