# Wind Turbine (Spark - Livy - Sparkmagic)

In this demonstration, you use Spark to explore a dataset and train a Gradient-Boosted Tree (GBT) regressor that
leverages various features, such as wind speed and direction, to estimate the power output of a wind turbine.

![wind-farm](images/wind-farm.jpg)

Wind turbines hold tremendous potential as a sustainable source of energy, capable of supplying a substantial portion
of the world's power needs. However, the inherent unpredictability of power generation poses a challenge when it comes
to optimizing this process.

Fortunately, you have a powerful tool at our disposal: Machine Learning (ML). By leveraging advanced algorithms and data
analysis, you can develop models that accurately predict the power production of wind turbines. This enables you to
optimize the power generation process and overcome the challenges associated with its ingrained variability.

1. [What You'll Need](#what-youll-need)
1. [Procedure](#procedure)
1. [How it Works](#how-it-works)
1. [References](#references)

## What You'll Need

For this tutorial, ensure you have:

- Access to an HPE Ezmeral Unified Analytics cluster.

## Procedure

To complete this tutorial follow the steps below:

1. Login to your Ezmeral Unified Analytics (EzUA) cluster, using your credentials.
1. Create a new Notebook server using the `jupyter-data-science` image. Request at least `4Gi` of memory for the
   Notebook server.
1. Connect to the Notebook server and clone the repository locally.
1. Navigate to the tutorial's directory (`ezua-tutorials/demos/wind-turbine`).
1. Launch a new terminal window and create a new conda environment using the specified `environment.yaml` file:
   ```
   conda env create -f environment.yaml
   ```
1. Add the new conda environment as an ipykernel:
   ```
   python -m ipykernel install --user --name=wind-turbine
   ```
1. Refresh your browser tab to access the updated environment.
1. Launch the `wind-turbine.ipynb` notebook file and follow the instructions. Make sure to select the `wind-turbine`
   environment kernel. 

## How it Works

In this tutorial, you use Livy and Sparkmagic to remotely execute Python code in a Spark cluster. Livy is an open-source
REST service that enables remote and interactive analytics on Apache Spark clusters. It provides a way to interact with
Spark clusters programmatically using a REST API, allowing you to submit Spark jobs, run interactive queries, and manage
Spark sessions.

To communicate with Livy and manage your sessions you use Sparkmagic, an open-source tool that provides a Jupyter kernel
extension. Sparkmagic integrates with Livy, to provide the underlying communication layer between the Jupyter kernel and
the Spark cluster.

## References

1. [Spark: Unified engine for large-scale data analytics](https://spark.apache.org/)
1. [Livy: A REST Service for Apache Spark](https://livy.apache.org/)
1. [Sparkmagic: Jupyter magics and kernels for working with remote Spark clusters](https://github.com/jupyter-incubator/sparkmagic)
1. [Wind Turbine Scada Dataset](https://www.kaggle.com/datasets/berkerisen/wind-turbine-scada-dataset/data)