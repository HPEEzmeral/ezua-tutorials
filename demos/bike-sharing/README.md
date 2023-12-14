# Bike Sharing (MLFlow - KServe)

This tutorial provides a detailed walkthrough of a comprehensive Machine Learning (ML) workflow, encompassing data
preprocessing, model training and evaluation, hyperparameter tuning, experiment tracking via MLflow [1], and model
deployment using Seldon and KServe [2]. The use case under consideration is the well-known bike sharing dataset, sourced
from the UCI ML Repository [3].

![bike-sharing](images/bike-sharing.jpg)

The dataset records the hourly and daily count of rental bikes between 2011 and 2012 in the Capital Bikeshare system,
supplemented with corresponding weather and seasonal data. The primary objective of this dataset is to foster research
into bike sharing systems, which are gaining significant attention due to their implications on traffic management,
environmental sustainability, and public health.

The task associated with this dataset is regression, with 17,389 instances. The overarching goal is to construct a
predictive model capable of forecasting bike rental demand.

1. [What You'll Need](#what-youll-need)
1. [Procedure](#procedure)
1. [How it Works](#how-it-works)
1. [Clean Up](#clean-up)
1. [References](#references)

## What You'll Need

For this tutorial, ensure you have:

- Access to an HPE Ezmeral Unified Analytics (EzUA) cluster.

## Procedure

To complete the tutorial follow the steps below:

1. Login to your EzUA cluster, using your credentials.
1. Create a new Notebook server using the `jupyter-data-science` image. Request at least 4Gi of memory for the Notebook
   server.
1. Connect to the Notebook server, launch a new terminal window, and clone the repository locally.
1. Navigate to the tutorial's directory (`ezua-tutorials/tutorials/mlflow`)
1. Create your virtual environment:
    - Deactivate the base conda environment:
        ```
        conda deactivate
        ```
    - Create a new virtual environment:
       ```
       python -m venv bike-sharing
       ```
    - Activate the new virtual environment:
       ```
       source bike-sharing/bin/activate
       ```
    - Upgrade `pip`:
       ```
       pip install --upgrade pip
       ```
    - Install the dependencies:
       ```
       pip install -r requirements.txt
       ```
    - Add the new conda environment as an ipykernel:
       ```
       python -m ipykernel install --user --name=bike-sharing
       ```
    - Refresh your browser tab to access the updated environment.
1. Launch the two Notebooks in order and execute the code cells. Make sure to select the `bike-sharing` environment
   kernel for each Notebook.

## How it Works

MLflow is an open-source platform designed to manage the end-to-end machine learning lifecycle. It encompasses tools for
tracking experiments, packaging code into reproducible runs, and sharing and deploying models.

With its tracking component, MLflow allows data scientists and engineers to log metrics, parameters, and artifacts for
each run, enabling easy comparison and reproducibility of experiments. The project component supports packaging ML code
so it can be easily shared or executed on other platforms. Finally, the model component simplifies model deployment
across diverse platforms.

Overall, MLflow provides a unified interface to collaborate, reproduce, and operationalize machine learning workflows,
ensuring consistency and transparency from experimentation to production.

## Clean Up

1. Go to the Kubeflow Endpoints UI and delete the Inference Service called `bike-sharing`.

## References

1. [MLflow - An open source platform to manage the ML lifecycle, including experimentation, reproducibility, deployment, and a central model registry](https://mlflow.org/)
1. [KServe - Highly scalable and standards based Model Inference Platform on Kubernetes for Trusted AI](https://kserve.github.io/website/0.11/)
1. https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset