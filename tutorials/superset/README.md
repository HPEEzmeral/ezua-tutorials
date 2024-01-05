# Data Connection and Visualization (Superset Tutorial)

This tutorial series will demonstrate how to work with external data sources within HPE Ezmeral Unified Analytics software. 
Leveraging EzPresto and Superset, you will create a dashboard displaying insights related to a real-world analytics use case. 

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
1. Create a new Notebook server using the `jupyter-data-science` image. Request at least `4Gi` of memory for the
   Notebook server.
1. Connect to the Notebook server, launch a new terminal window, and clone the repository locally.
1. Navigate to the tutorial's directory (`ezua-tutorials/tutorials/superset`).
1. Launch the Notebook files in order. Each Notebook file contains instructions on how to proceed.

## How it Works

This tutorial demonstrates how to connect external data sources to HPE Ezmeral Unified Analytics. Leveraging these datasets, this tutorial
will demonstrate how to run queries on tables within those datasets using EzPresto, HPE's own fork of Presto, the an open-source distributed
SQL query engine designed for fast and scalable data querying and analysis. The query results will then be displayed on Charts within Views
that are created in Apache Superset, an open-source data visualization and data exploration platform. 

In the final tutorial step, you will create a dashboard for a real-world retail use case.

## References

1. [Presto: Fast and Reliable SQL Engine for Data Analytics and the Open Lakehouse](http://prestodb.io)
1. [Superset: An open-source modern data exploration and visualization platform.](https://superset.apache.org)