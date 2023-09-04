import pyspark
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from math import radians
from warnings import filterwarnings

from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.sql.functions import substring
from pyspark.sql.types import IntegerType
from pyspark.sql import functions as F
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.regression import GBTRegressionModel
from pyspark.ml.evaluation import RegressionEvaluator
from py4j.java_gateway import java_import


sns.set_style('white')
filterwarnings('ignore')

java_import(spark._sc._jvm, "org.apache.spark.sql.api.python.*")

# Reading Dataset
spark_df = spark.read.csv(
    'file:///mounts/shared-volume/spark/T1.csv',
    header=True, inferSchema=True)

# Caching the dataset
spark_df.cache()

# Converting all the column names to lower case
spark_df = spark_df.toDF(*[c.lower() for c in spark_df.columns])

print('Show the first 5 rows')
print(spark_df.show(5))

print('What are the variable data types?')
print(spark_df.printSchema())

print('How many observations do we have?')
print(spark_df.count())

# Extracting a substring from columns to create month and hour variables
spark_df = spark_df.withColumn("month", substring("date/time", 4, 2))
spark_df = spark_df.withColumn("hour", substring("date/time", 12, 2))

# Converting string month and hour variables to integer
spark_df = spark_df.withColumn('month', spark_df.month.cast(IntegerType()))
spark_df = spark_df.withColumn('hour', spark_df.hour.cast(IntegerType()))

print(spark_df.show(5))

# Exploratory Data Analysis
pd.options.display.float_format = '{:.2f}'.format
spark_df.select('wind speed (m/s)', 'theoretical_power_curve (kwh)',
                'lv activepower (kw)').toPandas().describe()

# Taking a random sample from the big data
sample_df = spark_df.sample(withReplacement=False,
                            fraction=0.1, seed=42).toPandas()

# Visualizing the distributions with the sample data
columns = ['wind speed (m/s)', 'wind direction (deg)', 'month', 'hour',
           'theoretical_power_curve (kwh)', 'lv activepower (kw)']
i = 1
plt.figure(figsize=(10, 12))
for each in columns:
    plt.subplot(3, 2, i)
    sample_df[each].plot.hist(bins=12)
    plt.title(each)
    i += 1

# Question: Is there any difference between the months
# for average power production?

plt.clf()

# Average power production by month
monthly = (spark_df.groupby('month')
                   .mean('lv activepower (kw)')
                   .sort('avg(lv activepower (kw))')
                   .toPandas())
sns.barplot(x='month', y='avg(lv activepower (kw))', data=monthly)
plt.title('Months and Average Power Production')
print(monthly)

# Question: Is there any difference between the hours for average power
# production?

plt.clf()

# Average power production by hour
hourly = (spark_df.groupby('hour')
                  .mean('lv activepower (kw)')
                  .sort('avg(lv activepower (kw))')
                  .toPandas())
sns.barplot(x='hour', y='avg(lv activepower (kw))', data=hourly)
plt.title('Hours and Average Power Production')
print(hourly)

# Question: Is there any correlation between the wind speed,
# wind direction and power production?
pd.set_option('display.max_columns', None)
sample_df[columns].corr()
plt.clf()
sns.pairplot(sample_df[columns], markers='*')

# Question: What is the average power production level for
# different wind speeds?
# Finding average power production for 5 m/s wind speed increments
wind_speed = []
avg_power = []
for i in [0, 5, 10, 15, 20]:
    avg_value = (spark_df.filter((spark_df['wind speed (m/s)'] > i)
                                 & (spark_df['wind speed (m/s)'] <= i+5))
                         .agg({'lv activepower (kw)': 'mean'})
                         .collect()[0][0])
    avg_power.append(avg_value)
    wind_speed.append(str(i) + '-' + str(i+5))

plt.clf()
sns.barplot(x=wind_speed, y=avg_power, color='orange')
plt.title('Avg Power Production for 5 m/s Wind Speed Increments')
plt.xlabel('Wind Speed')
plt.ylabel('Average Power Production')

# Question: What is the power production for different wind directions and
# speeds?

# Creating the polar diagram
plt.clf()
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)
# Inside circles are the wind speed and marker color and size represents the
# amount of power production
sns.scatterplot(x=[radians(x) for x in sample_df['wind direction (deg)']],
                y=sample_df['wind speed (m/s)'],
                size=sample_df['lv activepower (kw)'],
                hue=sample_df['lv activepower (kw)'],
                alpha=0.7, legend=None)
# Setting the polar diagram's top represents the North
ax.set_theta_zero_location('N')
# Setting -1 to start the wind direction clockwise
ax.set_theta_direction(-1)
# Setting wind speed labels in a better position to see
ax.set_rlabel_position(110)
plt.title('Wind Speed - Wind Direction - Power Production Diagram')
plt.ylabel(None)

# Question: Does the manufacturer's theoritical power production curve fit
# well with the real production?

plt.clf()
plt.figure(figsize=(10, 6))
sns.scatterplot(x='wind speed (m/s)', y='lv activepower (kw)', color='orange',
                label='Real Production', alpha=0.5, data=sample_df)
sns.lineplot(x='wind speed (m/s)', y='theoretical_power_curve (kwh)',
             color='blue', label='Theoritical Production', data=sample_df)
plt.title('Wind Speed and Power Production Chart')
plt.ylabel('Power Production (kw)')

# Question: What is the wind speed threshold value for zero theorical power?
# Filter the big data where the real and theoritical power productions are
# equal to 0.
zero_theo_power = (spark_df.filter(
    (spark_df['lv activepower (kw)'] == 0)
    & (spark_df['theoretical_power_curve (kwh)'] == 0))
                           .toPandas())

print(zero_theo_power[['wind speed (m/s)', 'theoretical_power_curve (kwh)',
                       'lv activepower (kw)']].sample(5))
plt.clf()
# Let's see the wind speed distribution for 0 power production
zero_theo_power['wind speed (m/s)'].hist()
plt.title('Wind Speed Distribution for 0 Power Production')
plt.xlabel('Wind speed (m/s)')
plt.ylabel('Counts for 0 Power Production')

# Question: Why there aren't any power production in some observations while
# the wind speed is higher than 3 m/s?

# Observations for the wind speed > 3m/s and power production = 0,
# While theoritically there should be power production
zero_power = spark_df.filter((spark_df['lv activepower (kw)'] == 0)
                             & (spark_df['theoretical_power_curve (kwh)'] != 0)
                             & (spark_df['wind speed (m/s)'] > 3)).toPandas()
print(zero_power.head())
print('No of Observations (while Wind Speed > 3 m/s'
      ' and Power Production = 0): ', len(zero_power))

plt.clf()
zero_power['wind speed (m/s)'].plot.hist(bins=8)
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Counts for Zero Production')
plt.title('Wind Speed Counts for Zero Power Production')
plt.xticks(ticks=np.arange(4, 18, 2))

# Let's see the monthly distribution for zero power production.

plt.clf()
sns.countplot(zero_power['month'])

# Excluding the observations meeting the filter criterias
spark_df = spark_df.filter(~((spark_df['lv activepower (kw)'] == 0)
                             & (spark_df['theoretical_power_curve (kwh)'] != 0)
                             & (spark_df['wind speed (m/s)'] > 3)))
spark_df.show(20)

# Question: Is there any other outliers?

columns = ['wind speed (m/s)', 'wind direction (deg)',
           'theoretical_power_curve (kwh)', 'lv activepower (kw)']
i = 1
plt.clf()
plt.figure(figsize=(20, 3))
for each in columns:
    df = spark_df.select(each).toPandas()
    plt.subplot(1, 4, i)
    # plt.boxplot(df)
    sns.boxplot(x=df[each])
    plt.title(each)
    i += 1

# We will find the upper and lower threshold values for the wind speed data,
# and analyze the outliers.

# Create a pandas df for visualization
wind_speed = spark_df.select('wind speed (m/s)').toPandas()

# Defining the quantiles and interquantile range
Q1 = wind_speed['wind speed (m/s)'].quantile(0.25)
Q3 = wind_speed['wind speed (m/s)'].quantile(0.75)
IQR = Q3-Q1
# Defining the lower and upper threshold values
lower = Q1 - 1.5*IQR
upper = Q3 + 1.5*IQR

print('Quantile (0.25): ', Q1, '  Quantile (0.75): ', Q3)
print('Lower threshold: ', lower, ' Upper threshold: ', upper)

# Fancy indexing for outliers
outlier_tf = ((wind_speed['wind speed (m/s)'] < lower)
              | (wind_speed['wind speed (m/s)'] > upper))

print('Total Number of Outliers: ',
      len(wind_speed['wind speed (m/s)'][outlier_tf]))
print('--'*15)
print('Some Examples of Outliers:')
print(wind_speed['wind speed (m/s)'][outlier_tf].sample(10))

# Out of 47033, there is only 407 observations while the wind speed is over
# 19 m/s.
# Now Lets see average power production for these high wind speed
(spark_df.select('wind speed (m/s)', 'lv activepower (kw)')
         .filter(spark_df['wind speed (m/s)'] >= 19)
         .agg({'lv activepower (kw)': 'mean'})
         .show())

spark_df = spark_df.withColumn('wind speed (m/s)',
                               F.when(F.col('wind speed (m/s)') > 19.447, 19)
                               .otherwise(F.col('wind speed (m/s)')))
spark_df.count()

# Question: What are the general criterias for power production?

# High level power production
(spark_df.filter(
             ((spark_df['month'] == 3) | (spark_df['month'] == 8) | (spark_df['month'] == 11))
             & ((spark_df['hour'] >= 16) | (spark_df['hour'] <= 24))
             & ((spark_df['wind direction (deg)'] > 0) | (spark_df['wind direction (deg)'] < 90))
             & ((spark_df['wind direction (deg)'] > 180) | (spark_df['wind direction (deg)'] < 225)))
         .agg({'lv activepower (kw)': 'mean'})
         .show())

# Low level power production
(spark_df.filter(
             (spark_df['month'] == 7)
             & ((spark_df['hour'] >= 9) | (spark_df['hour'] <= 11))
             & ((spark_df['wind direction (deg)'] > 90) | (spark_df['wind direction (deg)'] < 160)))
         .agg({'lv activepower (kw)': 'mean'})
         .show())


# Data Preparation for ML Algorithms
# Preparing the independent variables (Features)
# Converting lv activepower (kw) variable as label
spark_df = spark_df.withColumn('label', spark_df['lv activepower (kw)'])

# Defining the variables to be used
variables = ['month', 'hour', 'wind speed (m/s)', 'wind direction (deg)']
vectorAssembler = VectorAssembler(inputCols=variables,
                                  outputCol='features')
va_df = vectorAssembler.transform(spark_df)

# Combining features and label column
final_df = va_df.select('features', 'label')
final_df.show(10)

# Train Test Split
splits = final_df.randomSplit([0.8, 0.2])
train_df = splits[0]
test_df = splits[1]

print('Train dataset: ', train_df.count())
print('Test dataset : ', test_df.count())

# Creating the Initial Model
# Creating the gbm regressor object
gbm = GBTRegressor(featuresCol='features', labelCol='label')

# Training the model with train data
gbm_model = gbm.fit(train_df)

# Predicting using the test data
y_pred = gbm_model.transform(test_df)

# Initial look at the target and predicted values
y_pred.select('label', 'prediction').show(20)

# Store our model in user shared volume
gbm_model.write().overwrite().save(
    'file:///mounts/shared-volume/spark/GBM.model')

gbm_model_dtap = GBTRegressionModel.load(
    "file:///mounts/shared-volume/spark/GBM.model")

# Let's evaluate our model's success
# Initial model success
evaluator = RegressionEvaluator(predictionCol='prediction', labelCol='label')

print('R2:\t', evaluator.evaluate(y_pred, {evaluator.metricName: 'r2'}))
print('MAE:\t', evaluator.evaluate(y_pred, {evaluator.metricName: 'mae'}))
print('RMSE:\t', evaluator.evaluate(y_pred, {evaluator.metricName: 'rmse'}))

# Comparing Real, Theoritical and Predicted Power Productions

# Converting sample_df back to Spark dataframe
eva_df = spark.createDataFrame(sample_df)

# Converting lv activepower (kw) variable as label
eva_df = eva_df.withColumn('label', eva_df['lv activepower (kw)'])

# Defining the variables to be used
variables = ['month', 'hour', 'wind speed (m/s)', 'wind direction (deg)']
vectorAssembler = VectorAssembler(inputCols=variables, outputCol='features')
vec_df = vectorAssembler.transform(eva_df)

# Combining features and label column
vec_df = vec_df.select('features', 'label')

# Using ML model to predict
preds = gbm_model.transform(vec_df)
preds_df = preds.select('label', 'prediction').toPandas()

# Compining dataframes to compare
frames = [sample_df[['wind speed (m/s)', 'theoretical_power_curve (kwh)']],
          preds_df]
sample_data = pd.concat(frames, axis=1)

plt.clf()
# Visualizing real, theoritical and predicted power production
plt.figure(figsize=(10, 7))
sns.scatterplot(x='wind speed (m/s)', y='label', alpha=0.5,
                label='Real Power', data=sample_data)
sns.scatterplot(x='wind speed (m/s)', y='prediction', alpha=0.7,
                label='Predicted Power', marker='o', data=sample_data)
sns.lineplot(x='wind speed (m/s)', y='theoretical_power_curve (kwh)',
             label='Theoritical Power', color='purple', data=sample_data)
plt.title('Wind Turbine Power Production Prediction')
plt.ylabel('Power Production (kw)')
plt.legend()

