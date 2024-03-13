## Ray Fibonacci Example

##### This example demonstrates the comparison between executing tasks locally and distributedly using Ray.

### Prerequisites:
* Ensure you are using a Data Science notebook environment in Kubeflow. 
* Ray client and server versions must match. Typically, `ray --version` can be used to verify the installed version. 
* Activate the Ray-specific Python kernel in your notebook environment. 
* To ensure optimal performance, use dedicated directories containing only the essential files needed for that job submission as a working directory.

### Turning Python Functions into Remote Functions (Ray Tasks):
To leverage Ray's distributed computing capabilities, regular Python functions can be submitted as Ray tasks using the `JobSubmissionClient`. 

Consider the following function that generates Fibonacci sequences (integer sequence in which every number after the first two is the sum of the two preceding ones.).
```python
def fibonacci_function(sequence_size):
    fibonacci = []
    for i in range(0, sequence_size):
        if i < 2:
            fibonacci.append(i)
            continue
        fibonacci.append(fibonacci[i-1]+fibonacci[i-2])
    return sequence_size
```
This function can be executed both as a regular Python function and as a Ray job for distributed execution.

### Comparing Local vs Remote Performance:
We compare the duration required to generate several long Fibonacci sequences, executing the tasks locally and using Ray. 
The objective is to showcase Ray's efficiency under heavy workloads. 

The execution approach is based on system resources as shown below:
```python
if __name__ == "__main__":
    n = int(sys.argv[1])
    start_time = time.time()
    [fibonacci_function(n) for _ in range(os.cpu_count())]
    end_time = time.time()
    duration = end_time - start_time
    print(f"Computation time for {n} sequence is {duration}")
```

Below is a screenshot showing the comparative performance results, illustrating Ray's effectiveness in handling intensive computational tasks:

![result-comparison.png](resources%2Fresult-comparison.png)
