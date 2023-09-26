<a name="br1"></a> 

**Whylogs with Airflow**

**Overview**

This guide explains how to use Whylogs with Apache Airﬂow to ensure data quality and

consistency. Whylogs is a data proﬁling library that allows you to monitor and analyze your

data over ꢀme.

In this use case, we will be using Apache Airﬂow to automate tasks related to data quality

and consistency checks using Whylogs. We have two datasets:

We are using a wine-quality dataset wherein one is reference data set and other is target

data set.

**Reference dataset:** This dataset serves as the historical reference data. We use it as a benchmark

to detect any data driꢁ in the target dataset.

**Target dataset** This dataset is the one we want to check for data quality, including driꢁ and

consistency.

**DAG workﬂow:**

1\. **Read and Profile the Target Data:**

This task involves reading the target dataset and using Whylogs to create a data profile.

**2. Read and Profile the Reference Data:**

Here, we read the reference dataset and create a data profile to serve as the baseline for

comparison.

**3. Check the Consistency of the Target Profile:**

In this step, we perform checks on the data profile of the target dataset to ensure

consistency.

4\. **Compare and Generate the Drift Report**:

Finally, we compare the data profiles of the target and reference datasets to identify any

data drift. A drift report is generated to highlight discrepancies.



<a name="br2"></a> 

**DAG summary:**

**Task Graph:**

The data proﬁles and the driꢁ summary report are stored in the shared volume and we can

download and view it.



<a name="br3"></a> 

**Driꢀ summary report:**

