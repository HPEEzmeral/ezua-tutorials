from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from ray import tune
import json
import numpy as np
import pandas as pd
import ray
import time
from ray import train
from ray import tune
from ray.tune.schedulers import ASHAScheduler

def parse_hn_submissions(path):
    with open(path, "r") as f:
        records = []
        for line in f.readlines():
            body = json.loads(line)["body"]
            records.append({"data": body["title"], "score": body["score"]})
        return pd.DataFrame(records)
    
    
start_time = time.time()

files = ["ls-" + str(i) + ".json" for i in range(1, 2)]
records = [parse_hn_submissions(file) for file in files]
df = pd.concat(records)

end_time = time.time()
duration = end_time - start_time
print("Took {} seconds to parse the hackernews submissions".format(duration))

df.head()

df["score"].median()

df["target"] = df["score"] > 1.0
         
from sklearn.model_selection import train_test_split
train_0, test = train_test_split(df, test_size=0.2)
         
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier

pipeline = Pipeline([
    ("vect", CountVectorizer()),
    ("clf", SGDClassifier(loss="hinge", penalty="l2",
                          alpha=0.001,
                          max_iter=5, tol=1e-3,
                          warm_start=True))])
result = pipeline.fit(train_0.data, train_0.target)

predicted = result.predict(train_0.data)
print("Accuracy on the training set is {}".format(np.mean(predicted == train_0.target)))
         
         
predicted = pipeline.predict(test.data)
print("Accuracy on the test set is {}".format(np.mean(predicted == test.target)))
pipeline.predict(["Iconic consoles of the IBM System/360 mainframes, 55 years old today", "Are Banned Drugs in Your Meat?"])  

train_id = ray.put(train_0)
test_id = ray.put(test)

def train_func(config):
    pipeline = Pipeline([
    ("vect", CountVectorizer()),
    ("clf", SGDClassifier(loss="hinge", penalty="l2",
                          alpha=config["alpha"],
                          max_iter=5, tol=1e-3,
                          warm_start=True))])
    train_1 = ray.get(train_id)
    test = ray.get(test_id)
    for i in range(5):
        # Perform one epoch of SGD
        X = pipeline.named_steps["vect"].fit_transform(train_1.data)
        pipeline.named_steps["clf"].partial_fit(X, train_1.target, classes=[0, 1])
        
        # ray:2.7.0: migration
        print("=========1", np.mean(pipeline.predict(test.data)))
        print("=========2", test.target)
        print("=========3", test.data)
        train.report({'mean_accuracy': np.mean(pipeline.predict(test.data))})
        
analysis = tune.run(
                train_func,
                config={"alpha": tune.grid_search([1e-3, 1e-4, 1e-5, 1e-6])},
                resources_per_trial={"cpu": 3},
                metric="mean_accuracy",
                mode="max",
                num_samples=1,
                reuse_actors=True,
                stop={
                    "mean_accuracy": 0.50, 
                    "training_iteration": 1},
                scheduler=ASHAScheduler(max_t=5),
                raise_on_failed_trial=False
            )

best_trial = analysis.get_best_trial(metric="mean_accuracy", mode="max", scope="all")
print("FINAL SUCCESSFULLY EXECUTED ===== ", best_trial)