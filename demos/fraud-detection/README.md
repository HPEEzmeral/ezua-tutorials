# Fraud Detection (Pipelines - Serving)

Fraudulent activity has permeated multiple sectors, from e-commerce and healthcare to banking and payment systems. This illicit industry amasses billions every year and is on an upward trajectory. The 2018 global economic crime survey by PwC verifies this assertion, revealing that 49 percent of the 7,200 enterprises surveyed had fallen prey to some form of fraudulent conduct.

![fraud-detection-banking](images/artboard.png)

Despite the perceived peril of fraud to businesses, the advent of sophisticated systems, such as rule engines or machine learning, equips us with the tools to detect and prevent such behaviors. In this notebook, we demonstrate how a machine learning system helps us achieve this.

At its core, a rules engine is a sophisticated software system that enforces one or more business rules in a real-time production environment. More often than not, these rules are the crystallization of hard-earned insights gleaned from domain experts. For instance, we could establish rules limiting the number of transactions in a given time frame, and blocking transactions that originate from previously identified fraudulent IPs and/or domains. Such rules prove highly effective in detecting certain types of fraud, yet they are not without their limitations. Rules with predefined threshold values may give rise to false positives or false negatives. To illustrate, imagine a rule that rejects any transaction exceeding \\$10,000 for a particular user. A seasoned fraudster might exploit this by staying one step ahead, consciously making a transaction slightly below this threshold (for instance, \\$9,999), thereby evading detection.

This is where machine learning comes to the rescue: By reducing both the risk of fraud and potential financial losses to businesses, machine learning fortifies the efficacy of the detection system. Combining this technology with rules-based systems ensures that fraud detection becomes a more precise and reliable endeavor. In our exploration, we will be inspecting fraudulent transactions using the Banksim dataset. This synthetically created dataset is an combination of various customer payments, made at different intervals and in varying amounts. Through this, we aim to provide a comprehensive understanding of how we can detect and curtail fraudulent activities with high accuracy.

## What You'll Need

To complete the tutorial follow the steps below:

1. Login to Ezmeral Unified Analytics cluster.
1. Create a new notebook server using the `jupyter-data-science` image.
1. Launch the `experiment.ipynb` notebook file.
1. Run the first section of the Notebook (i.e., "Imports & Initialization") to upload the datase to object storage.
1. Enable the Kale Jupyter extension from the left side panel.
1. Click on the compile and run button and wait for Kale to compile your Notebook and submit the pipeline.
1. Wait until the pipeline completes and submits an Inference service.
1. Return to the Notebook and run the cells that:
  - Import the necessary modules and set the configuration.
  - Define the helper functions.
1. Run the `Prediction` section of the Notebook to invoke the inference service.
