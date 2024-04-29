## Ray Serve Example: Deploying a Rent Forecast Model

##### This guide demonstrates a comprehensive workflow for developing a machine learning model to predict rental prices, evaluating its performance, and deploying it for real-time inference using Ray Serve.

### Prerequisites:
* Ensure you are using a Data Science notebook environment in Kubeflow.
* Ray client and server versions must match. Typically, `ray --version` can be used to verify the installed version.
* Activate the Ray-specific Python kernel in your notebook environment.
* To ensure optimal performance, use dedicated directories containing only the essential files needed for that job submission as a working directory.

### From Training to Prediction: Deploying a Rent Forecast Model with Ray Serve

#### 1. Data and Model Management

* **Generate Model Data:** Initially, create synthetic data to train the prediction model:
![1_generating_data.png](resources%2F1_generating_data.png)


* **Prepare Data for the Model:** Format and supply the generated data to the model for training:
![2_preparing_data_model.png](resources%2F2_preparing_data_model.png)


* **Visualize the Model Performance:** Visualization aids in better understanding the model's performance:
![3_plotting_model.png](resources%2F3_plotting_model.png)

#### 2. Application Deployment

* **Prepare the Application:** Set up an application with Ray Serve, ensuring the model is correctly referenced during creation:
![4_application.png](resources%2F4_application.png)


* **Build Configuration File:** Execute the `serve build` command to generate a configuration file within the same directory.
![5_serve_build.png](resources%2F5_serve_build.png)


* **Temporary Workaround:** Due to a current limitation where `serve deploy` does not recognize the `--working-dir` option (track progress at Ray Issue https://github.com/ray-project/ray/issues/29354), a temporary workaround involves using `JobSubmissionClient` to manually push files to the Ray Cluster.
![6_workaround.png](resources%2F6_workaround.png)


* **Deploy the Application:** With the configuration file adjusted to push the necessary files, proceed to deploy the application to the Ray Cluster:
![7_deployment.png](resources%2F7_deployment.png)

#### 3. Monitoring and Prediction

* **Monitor Deployment:** View the deployed application in the Ray Dashboard under the Serve tab:
![ray_dashboard_serve.png](resources%2Fray_dashboard_serve.png)


* **Request Predictions:** Once the application is in a `running` state, it's ready to process prediction requests:
![8_prediction.png](resources%2F8_prediction.png)

#### 4. Shutdown

* **Terminate Deployment:** Use the `serve shutdown` command to cleanly shut down the deployment:
![9_shutdown.png](resources%2F9_shutdown.png)
