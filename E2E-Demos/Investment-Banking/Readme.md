# Investment Banking
Predict if the client will subscribe to a Investment Banking based on the analysis of the marketing campaigns the bank performed.

### Dataset
- Minio Setup: Begin by creating a bucket named "bank" in the Minio storage. Upload a file with the format "bankyyyy-mm-dd.csv" into this bucket.

- MySQL Configuration: Create a table in your MySQL database using the "bankyyyy-mm-dd" format.

### Airflow Configuration
Establish connections in the Airflow UI. Create a connection named "df_s3" with type "Amazon Web Services" and provide the necessary configuration including endpoint URL, access key, secret access key, and other settings. Also, create a connection named "mysql_bank" with type "mysql" and provide details such as hostname, schema, login ID, password, and port.
- Triggering the DAG: Activate your DAG (Data Extraction DAG) and initiate the tasks by clicking on the trigger button.
- Spark ETL: Place the Spark YAML file in the same location as the DAG file and then trigger the DAG to execute the Spark ETL process. Place the spark application code file inside spark folder in shared volume.

### Spark Magic
Follow the steps below:
- Login to you EzAF cluster.
- Create a new notebook server using the jupyter-data-science image.
- Clone the repository locally.
- Place the Spark-Magics.ipynb and execute it.
- Select Add Endpoint.
- Select Single Sign-On.
- Select Create Session with relevant properties like spark.hadoop.fs.s3a.access.key etc. 
- Provide a name select python and click Create Session.
- When your session is ready the Manage Sessions pane will become active, providing you the session ID. The session state will become idle which means that you are good to go!

### Jupyter Notebook
To complete the tutorial follow the steps below:
- Login to you EzAF cluster.
- Create a new notebook server using the jupyter-data-science image.
- Clone the repository locally.
- Launch the Banking-exp.ipynb notebook file and run all the cells give relevant credentials for backend access.

### Mlflow
The model artifact is saved in s3 with details of each model like accuracy, mae, r2 score and root mean square error(RMSE) which can be accessed through the front end of ml flow for details of the models.

### Kubeflow
To complete the tutorial:
- Go to kale deployment panel in jupyter notebook
- Select the experiment “bank-demo”.
- Select compile and run.
- Let the pipeline execute.

### EzPresto
Add Data Source in HIVE:
   - Set Hive metastore as "discovery."
   - Provide details about the file, including its name, file type, and data directory (S3 bucket URL).
   - Include Hive S3 AWS access key, AWS secret key, S3 endpoint, and S3 path style access.
   - Click on "connect" to establish the data source.
Cache Data Source in Superset:
   - Navigate to the data catalog.
   - Select the recently added data source.
   - Click on "selected datasources."
   - Choose "cache datasets" to ensure accessibility in Superset.
### Superset
- Open the settings and navigate to "Database Connections."
- Add a new database and select Presto as the database type.
- Provide the URI in the format: 
```bash 
presto://ezpresto.hpe-cluster-name-ezaf.com:443/cache
```
- After successfully establishing the connection, proceed to the "Dashboards" section.
- Create a new dashboard and add new charts to it. Alternatively, you can include charts you've previously created.
- If you're adding existing charts, remember to edit the dataset accordingly before adding them to the dashboard.

### Grafana
Installing Grafana Using Helm Charts:
1.	Access the master node of the cluster and execute the following commands:
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install my-release grafana/Grafana -n prometheus
```
2.	To obtain the Grafana login password, run the command below: 
```bash 
kubectl get secret --namespace prometheus my-release-grafana -o jsonpath=”{.data.admin-password}” |base64 –decode; echo
```
3.	Create a virtual service by executing the following command:
```bash 
Kubectl apply -f grafana.yaml
```
After following these steps, you can access the Grafana UI using the defined host link in the YAML file.
Adding data sources:
- Navigate to the home options and click on "Data Sources."
- Choose "Prometheus" as the data source.
- Add the HTTP URL: http://af-prometheus-kube-prometh-prometheus:9090/
- Click "Save and Test."
Creating the dashboards:
- Go to the dashboard section and click "New" followed by "Import."
- Upload your dashboard's JSON file and import it.
- Customize variables from the dashboard settings as needed.

For importing dashboards refer to this git repo: https://github.com/knative-extensions/monitoring/tree/main/grafana