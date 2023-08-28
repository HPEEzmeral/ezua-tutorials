## Simple instructions to run experiments.

## EXAMPLE-1
With defined custom NAS/network storage path
To complete the tutorial follow simple steps below:
1. Login to you EzAF cluster.
2. Create a new notebook server using the `jupyter-data-science` image.
3. Clone the repository locally.
4. Launch the `ray-custom-storage-path.ipynb` notebook file.
5. This example will executes a log on top of RAY cluster.
6. Referes to the NAS/ Storage path and create dynamically the value on top individual {value}.txt file and print the sum after reading all generated files.

## EXAMPLE-2
With defined custom MINIO/S3 network storage path
To complete the tutorial follow simple steps below:
1. Login to you EzAF cluster.
2. Create a new notebook server using the `jupyter-data-science` image.
3. Clone the repository locally.
4. Launch the `ray-custom-s3-storage-path.ipynb` notebook file.
5. This example will executes a log on top of RAY cluster.
6. Referes to the MINIO/S3 Storage path and create dynamically the value on top individual {value}.txt file and print the sum after reading all generated files.