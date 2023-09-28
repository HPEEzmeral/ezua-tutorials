# Bike Sharing (Feast)

This tutorial explores how to leverage Feast for generating training data and enhancing online model inference. In this
use-case, your goal is to train a ride-sharing driver satisfaction prediction model using a training dataset built
using Feast.

1. [What You'll Need](#what-youll-need)
1. [Procedure](#procedure)
1. [References](#references)

## What You'll Need

For this tutorial, ensure you have:

- Access to an HPE Ezmeral Unified Analytics cluster.

## Procedure

To complete the tutorial follow the steps below:

1. Login to your Ezmeral Unified Analytics (EzUA) cluster, using your credentials.
1. Create a new Notebook server using the `jupyter-data-science` image. Request at least `4Gi` of memory for the
   Notebook server.
1. Connect to the Notebook server and clone the repository locally.
1. Navigate to the tutorial's directory (ezua-tutorials/tutorials/feast).
1. Lauch a new terminal window and create a new conda environment using the specified `environment.yaml` file:
   ```
   conda env create -f environment.yaml
   ```
1. Add the new conda environment as an ipykernel:
   ```
   python -m ipykernel install --user --name=ride-sharing
   ```
1. Refresh your browser tab to access the updated environment.
1. Launch the `ride-sharing.ipynb` Notebook and execute the code cells. Make sure to select the `ride-sharing`
   environment kernel.

## References

1. [Feast: Open Source Feature Store for Production ML](https://feast.dev/)