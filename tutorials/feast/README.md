# Ride Sharing (Feast)

This tutorial explores how to leverage Feast [1] for generating training data and enhancing online Machine Learning (ML)
model inference. In this use-case, your goal is to train a ride-sharing driver satisfaction prediction model using a
training dataset built using Feast.

1. [What You'll Need](#what-youll-need)
1. [Procedure](#procedure)
1. [How it Works](#how-it-works)
1. [References](#references)

## What You'll Need

For this tutorial, ensure you have:

- Access to an HPE Ezmeral Unified Analytics (EzUA) cluster.

## Procedure

To complete the tutorial follow the steps below:

1. Login to your EzUA cluster, using your credentials.
1. Create a new Notebook server using the `marketplace.us1.greenlake-hpe.com/ezmeral/ezkf/jupyter:v1.3.0-e658264`
   image. Request at least `4Gi` of memory for the Notebook server.
1. Connect to the Notebook server, launch a new terminal window, and clone the repository locally.
1. Navigate to the tutorial's directory (`ezua-tutorials/tutorials/feast`).
1. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
1. Refresh your browser tab to access the updated environment.
1. Launch the `ride-sharing.ipynb` Notebook and execute the code cells.

## How it Works

Feast is an open-source platform designed to manage, store, and serve ML features to production models. At its core,
Feast decouples the feature engineering process from model training and serving. Engineers and data scientists define
and compute features, then store them in the Feast feature store. Once in the store, these features can be retrieved for
both training ML models and serving them in real-time or batch predictions.

The central feature store ensures consistency in feature values and computation logic between training and serving,
reducing the possibility of training-serving skew. Additionally, Feast handles data backfills, versioning, and
monitoring, simplifying many of the operational complexities associated with deploying ML models at scale.

## References

1. [Feast: Open Source Feature Store for Production ML](https://feast.dev/)
