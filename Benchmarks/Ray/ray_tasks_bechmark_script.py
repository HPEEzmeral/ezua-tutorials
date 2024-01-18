from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import time
import ray
from ray.job_submission import JobSubmissionClient
import time

'''
Ray Scalability Envelope::
'''
class EzRayBenchmarkScript:
    def __init__(self):
        self._address = "10.224.226.40"
        self._num_cpus = 1
        self._port = 8265
        self._small_accelerate_limit= 10
        self._mid_accelerate_limit=100
        self._large_accelerate_limit=1000
        self._ray_address = f"http://{self._address}:{self._port}"

if __name__ == "__main__":
    # Start Ray.
    runobj = EzRayBenchmarkScript()
    # ray.init(address=runobj._address)
    
    # Submit Ray job using JobSubmissionClient
    client = JobSubmissionClient(runobj._ray_address)
    job_id = client.submit_job(
        entrypoint="",
        runtime_env={
            "working_dir": "./", 
            # "excludes": ['']
        }
    )

    # Define a remote functions.
    @ray.remote(num_cpus=runobj._num_cpus)
    def run_fun(x):
        return x

    # Wait for everything to start.
    time.sleep(1)

    # Defined a counter that continually increments to avoid speedups from previously cached results.
    i = 0

    # Benchmark submitting tasks.
    start = time.time()
    results = []
    for _ in range(runobj._small_accelerate_limit):
        results.append(run_fun.remote(i))
        i += 1
    end = time.time()
    print("Submitting one task took on average {}ms.".format(end - start))
    
    # Wait for the benchmark to finish.
    ray.get(results)

    # Benchmark submitting 100 task and getting the result.
    start = time.time()
    for _ in range(runobj._mid_accelerate_limit):
        # Wait for the benchmark to finish.
        ray.get(run_fun.remote(i))
        i += 1
    end = time.time()
    print("Submitting one task and getting the result took on average ""{}ms.".format(end - start))

    # Benchmark submitting one thousand tasks and getting the results.
    start = time.time()
    for _ in range(10):
        results = []
        for _ in range(runobj._large_accelerate_limit):
            results.append(run_fun.remote(i))
            i += 1
        # Wait for the benchmark to finish.
        ray.get(results)
    end = time.time()
    print("Submitting one thousand tasks and getting the results took on average ""{}ms.".format((end - start) * 100))

    # Benchmark composing ten tasks and getting the result.
    start = time.time()
    for _ in range(runobj._large_accelerate_limit):
        x = i
        i += 1
        for _ in range(runobj._small_accelerate_limit):
            x = run_fun.remote(x)
        # Wait for the benchmark to finish.
        ray.get(x)
    end = time.time()
    print("Composing ten tasks and getting the result took on average ""{}ms".format(end - start))

    # Benchmark putting a small array in the object store.
    values = [np.random.normal(size=1) for _ in range(runobj._large_accelerate_limit)]
    start = time.time()
    value_ids = [ray.put(value) for value in values]
    end = time.time()
    print("Putting an array of size 1 took on average {}ms".format(end - start))

    # Benchmark getting a small array.
    start = time.time()
    [ray.get(value_id) for value_id in value_ids]
    end = time.time()
    print("Getting an array of size 1 took on average {}ms".format(end - start))

    # Benchmark putting a larger array in the object store.
    values = [np.random.normal(size=runobj._large_accelerate_limit) for _ in range(runobj._small_accelerate_limit)]
    start = time.time()
    value_ids = [ray.put(value) for value in values]
    end = time.time()
    print("Putting an array of size 100000 took on average " "{}ms".format((end - start) * 100))

    # Benchmark getting a larger array.
    start = time.time()
    [ray.get(value_id) for value_id in value_ids]
    end = time.time()
    print("Getting an array of size 100000 took on average " "{}ms".format((end - start) * 100))
