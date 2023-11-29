# Stock Price Prediction
The use case is to demonstrate the data streaming capability of HPE Ezmeral Unified Analytics by streaming the stock price data of different companies listed in the National Stock Exchange of India. Additionally the stock prices are forecasted by deploying an LSTM model using Kserve as well as pipelines are defined for retraining the model whenever required.

![image](https://github.com/snairharikrishnan/ezua-tutorials/assets/68279057/074d651a-5bdc-4dac-b8ac-331e3161a2cd)

### Spark Sessions
Spark session is created with the predefined Spark cluster configuration.Apache Livy on the HPE Ezmeral platform enables programmatic, fault-tolerant, multi-tenant submission of Spark jobs from web/mobile apps (no Spark client needed). So, multiple users can interact with the Spark cluster concurrently and reliably. 

### MySQL Database
A Mysql database is created in Microsoft Azure and the streaming data which is read batch by batch is appended to it.

### Superset and EzPresto
The database is connected to both EzPresto and Superset. While EzPresto provides big query editor, Superset proivdes live dashboard on the data.

### Model Building
The stock price of one company is forecasted using a recurrent neural network model like LSTM.

### MLFlow
An experiment is registered in the mlflow tracking service, and different runs care carried out with different parameters and features. The parameters can then be logged in mlflow which can then be viewed on the UI. Different runs are then compared and the model with the best metric is chosen as the model to be moved to production.

### Inference Service
The best model which was chosen from the mlflow experiment is then deployed using KServe.Initially the service account with minio object store secret is scripted followed by the inference service (yaml files). Next, a new model server must be created in Kubeflow and this yaml file has to be uploaded. The inference service will now be created and once it is running, we can send our test data through REST APIs and get the response.

### Model Retraining Pipeline
A Kubeflow pipeline is designed to carry out each step of the model building process.

Refer the blogs for more information
