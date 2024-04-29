## Ray Hyperparameter Example

##### This example demonstrates hyperparameter tuning in a distributed computing environment using Ray, specifically applied to training a news recommendation system.

### Prerequisites:
* Ensure you are using a Data Science notebook environment in Kubeflow.
* Ray client and server versions must match. Typically, `ray --version` can be used to verify the installed version.
* Activate the Ray-specific Python kernel in your notebook environment.
* To ensure optimal performance, use dedicated directories containing only the essential files needed for that job submission as a working directory. `json` data files are located in the `resources` directory.

### News Recommendation System
The objective is to develop a simple yet effective news recommendation system. We will:

* **Prepare Training Data**: Utilize Ray to parallelize the data preparation process. 
* **Model Training**: Employ scikit-learn to train a model distinguishing between "popular" and "less popular" news articles. 
* **Hyperparameter Optimization**: Use Ray Tune, a library for scalable hyperparameter tuning, to find optimal model settings.

Ensure the necessary files, including data and configuration JSONs, are uploaded to your working directory as illustrated below:

![hyperparameter-working-dir.png](resources%2Fhyperparameter-working-dir.png)

Upon successful execution, the best training function settings determined through hyperparameter optimization will be displayed, as shown here:

![hyperparameter-result.png](resources%2Fhyperparameter-result.png)
