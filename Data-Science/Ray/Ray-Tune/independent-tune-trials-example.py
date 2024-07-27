from ray import tune
from ray import train
from ray.train import RunConfig
import ray
import os

NUM_MODELS = 5

def train_model(config):
    score = config["model_id"]

    # Import model libraries, etc...
    # Load data and train model code here...

    # Return final stats. You can also return intermediate progress
    # using ray.train.report() if needed.
    # To return your model, you could write it to storage and return its
    # URI in this dict, or return it as a Tune Checkpoint:
    # https://docs.ray.io/en/latest/tune/tutorials/tune-checkpoints.html
    return {"score": score, "other_data": ...}

# Define trial parameters as a single grid sweep.
trial_space = {
    # This is an example parameter. You could replace it with filesystem paths,
    # model types, or even full nested Python dicts of model configurations, etc.,
    # that enumerate the set of trials to run.
    "model_id": tune.grid_search([
        "model_{}".format(i)
        for i in range(NUM_MODELS)
    ])
}

# Can customize resources per trial, here we set 1 CPU each.
train_model = tune.with_resources(train_model, {"cpu": 1})

# Start a Tune run and print the best result.
tuner = tune.Tuner(train_model, param_space=trial_space)
results = tuner.fit()

# Access individual results.
print(results[0])
print(results[1])
print(results[2])
