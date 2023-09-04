# EzUA Tutorials

Welcome to the EzUA Tutorials repository! This is the official source for tutorials related to the EzUA platform.
The HPE Ezmeral Unified Analytics Software is usage-based Software-as-a-Service (SaaS) that fully manages, supports,
and maintains hybrid and multi-cloud modern analytical workloads through open-source tools.
The software separates compute and storage for flexible, cost-efficient scalability to securely access data
stored in multiple data platforms through a simple user interface, which is easily installed and deployed
in minutes on private, public, and on-premises infrastructure.

Whether you're a beginner or an advanced user, you'll find useful content to help you make the most out of EzUA's capabilities.

![ezua-tutorials](images/ezua-tutorials.jpg)

## Repository Structure

This repository is organized into two main directories:

- [Integration Tutorials](integration-tutorials): Tutorials that demonstrate how to integrate various applications
  like Kubeflow, Feast, Spark, and MLflow within the EzUA platform.
- [Applications](applications): Specialized tutorials tailored to specific applications.

### Integration Tutorials

Navigate to the [`integration-tutorials`]((integration-tutorials)) directory to find a collection of tutorials that cover a wide array of topics in analytics
and data science. These tutorials are designed to help you grasp the foundational elements of working within EzUA.

### Application-Specific Tutorials

For tutorials that are tailored to specific applications, go to the [`applications`](applications) directory.
You'll find specialized guides that show you how to leverage EzUA's tools for particular use-cases.
The current list of application-specific tutorials include:

- [FEAST feature store](applications/feast/): Ride sharing tutorial
- [Kubeflow Pipelines](applications/kubeflow-pipelines/): Financial time series tutorial
- [MLflow](applications/mlflow): Bike sharing tutorial
- [RAY](applications/ray): News recommendation tutorial

## Getting Started

To get started you need access to an EzUA cluster. Then:

1. Clone this repository:

    ```bash
    git clone https://github.com/HPEEzmeral/ezua-tutorials.git
    ```

2. Navigate to the desired directory.
3. Follow the README in the respective directory for further instructions.

## Requirements

These tutorials assume you have a basic understanding of Python programming and some familiarity with analytics and data science concepts.
Each tutorial may have additional specific requirements, which will be detailed within.