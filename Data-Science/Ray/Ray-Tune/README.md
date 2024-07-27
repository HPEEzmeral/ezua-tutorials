## Ray Tune Example

#### This example demonstrates a basic tune experiment in a distributed computing environment using Ray, specifically running indepedent trials in parallel.

### Prerequisites:
* Ensure you are using a Data Science notebook environment in Kubeflow.
* Ray client and server versions must match. Typically, `ray --version` can be used to verify the installed version.
* Activate the Ray-specific Python kernel in your notebook environment.
* To ensure optimal performance, use dedicated directories containing only the essential files needed for that job submission as a working directory. `json` data files are located in the `resources` directory.

### Running Independent Tune Trials in Parallel https://docs.ray.io/en/releases-2.24.0/tune/tutorials/tune-run.html



