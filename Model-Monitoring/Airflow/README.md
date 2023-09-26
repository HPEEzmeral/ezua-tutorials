# Whylogs with Airflow

### Overview

This guide explains how to use Whylogs with Apache Airﬂow to ensure data quality and

consistency. Whylogs is a data proﬁling library that allows you to monitor and analyze your

data over time.

In this use case, we will be using Apache Airﬂow to automate tasks related to data quality

and consistency checks using Whylogs. We have two datasets:

We are using a wine-quality dataset wherein one is reference data set and other is target

data set.

**Reference dataset:** This dataset serves as the historical reference data. We use it as a benchmark

to detect any data driꢁ in the target dataset.

**Target dataset** This dataset is the one we want to check for data quality, including driꢁ and

consistency.

### DAG workﬂow:

**1. Read and Profile the Target Data:**

This task involves reading the target dataset and using Whylogs to create a data profile.

**2. Read and Profile the Reference Data:**

Here, we read the reference dataset and create a data profile to serve as the baseline for

comparison.

**3. Check the Consistency of the Target Profile:**

In this step, we perform checks on the data profile of the target dataset to ensure

consistency.

**4. Compare and Generate the Drift Report**:

Finally, we compare the data profiles of the target and reference datasets to identify any

data drift. A drift report is generated to highlight discrepancies.




### DAG summary:
![image](https://github.com/HPEEzmeral/ezua-tutorials/assets/70695037/63a16a55-1408-4512-9ed4-e9513eec5afb)


![image](https://github.com/HPEEzmeral/ezua-tutorials/assets/70695037/35c6b93a-3ff5-40b8-82b3-7df693de6ad3)


### Task Graph:
![image](https://github.com/HPEEzmeral/ezua-tutorials/assets/70695037/fe981207-a672-4a78-98aa-fbdb30e20207)

The data proﬁles and the driꢁ summary report are stored in the shared volume and we can
download and view it.
![image](https://github.com/HPEEzmeral/ezua-tutorials/assets/70695037/f368dae3-9d2f-44cd-b05d-51eb1324b3cc)



### Drift summary report:
![image](https://github.com/HPEEzmeral/ezua-tutorials/assets/70695037/5f302556-1e56-49f3-856e-5e9cc9a75e0a)

