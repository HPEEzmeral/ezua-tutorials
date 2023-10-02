# Bike Sharing (MLFlow - KServe)

![bike-sharing](images/bike-sharing.jpg)

This tutorial provides a detailed walkthrough of a comprehensive data science workflow, encompassing data preprocessing,
model training and evaluation, hyperparameter tuning, experiment tracking via MLFlow, and model deployment using Seldon
and KServe. The use case under consideration is the well-known bike sharing dataset, sourced from the UCI Machine
Learning Repository.

The dataset records the hourly and daily count of rental bikes between 2011 and 2012 in the Capital Bikeshare system,
supplemented with corresponding weather and seasonal data. The primary objective of this dataset is to foster research
into bike sharing systems, which are gaining significant attention due to their implications on traffic management,
environmental sustainability, and public health.

The task associated with this dataset is regression, with 17,389 instances. The overarching goal is to construct a
predictive model capable of forecasting bike rental demand.

## What You'll Need

To complete the tutorial you'll need:

- Access to an HPE Ezmeral Unified Analytics cluster.

## Procedure

To complete the tutorial follow the steps below:

1. Login to the Ezmeral Unified Analytics cluster.
1. Create a new Notebook server using the `jupyter-data-science` image. Request at least 4Gi of memory for the Notebook
   server.
1. Connect to the Notebook server and clone the repository locally.
1. Create a new conda environment using the specified `environment.yaml` file:
   ```
   conda env create -f environment.yaml
   ```
1. Add the new conda environment as an ipykernel:
   ```
   python -m ipykernel install --user --name=bike-sharing
   ```
1. Refresh you browser tab, so the new environment will become available.
1. Launch the two Notebooks in order and execute the code cells. Make sure to select the `bike-sharing` environment
   kernel for each Notebook.

## References

1. https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset
1. https://docs.databricks.com/_static/notebooks/gbt-regression.html
1. https://www.kaggle.com/pratsiuk/mlflow-experiment-automation-top-9
1. https://mlflow.org/docs/latest/tracking.html
