# Data Connection and Visualization (Superset Tutorial)

This tutorial series will guide you through the process of integrating external data sources with
HPE Ezmeral Unified Analytics. Furthermore, using EzPresto and Superset, you'll learn to construct a
dashboard that presents insightful analysis pertaining to a practical real-world analytics scenario.

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
1. Create a new Notebook server using the `jupyter-data-science` image. Request at least `4Gi` of
   memory for the Notebook server.
1. Connect to the Notebook server, launch a new terminal window, and clone the repository locally.
1. Navigate to the tutorial's directory (`ezua-tutorials/tutorials/superset`).
1. Launch the Notebook files in order. Each Notebook file contains instructions on how to proceed.

## How it Works

This tutorial provides step-by-step instructions on integrating external data sources with HPE EzUA.
By accessing these datasets, you'll learn how to execute queries on tables within them using
EzPresto, HPE's specialized version of the open-source distributed SQL query engine renowned for its
rapid and scalable data querying and analysis capabilities. The outcomes of these queries will be
illustrated through Charts within Views crafted in Apache Superset, an open-source platform for data
visualization and exploration.

## References

1. [Presto: Fast and Reliable SQL Engine for Data Analytics and the Open Lakehouse](http://prestodb.io)
1. [Superset: An open-source modern data exploration and visualization platform.](https://superset.apache.org)