import os
import time
import ray

# Normal Python
def fibonacci_local(sequence_size):
    fibonacci = []
    for i in range(0, sequence_size):
        if i < 2:
            fibonacci.append(i)
            continue
        fibonacci.append(fibonacci[i-1]+fibonacci[i-2])
    return sequence_size

# Ray task
@ray.remote
def fibonacci_distributed(sequence_size):
    fibonacci = []
    for i in range(0, sequence_size):
        if i < 2:
            fibonacci.append(i)
            continue
        fibonacci.append(fibonacci[i-1]+fibonacci[i-2])
    return sequence_size

# Normal Python
def run_local(sequence_size):
    start_time = time.time()
    results = [fibonacci_local(sequence_size) for _ in range(os.cpu_count())]
    duration = time.time() - start_time
    print('Sequence size: {}, Local execution time: {}'.format(sequence_size, duration))

# Ray
def run_remote(sequence_size):
    # Starting Ray
    start_time = time.time()
    results = ray.get([fibonacci_distributed.remote(sequence_size) for _ in range(os.cpu_count())])
    duration = time.time() - start_time
    print('Sequence size: {}, Remote execution time: {}'.format(sequence_size, duration))

ray.init(address="ray://kuberay-head-svc.kuberay:10001")
print('Comparison of sequence size of 10000')
run_local(10000)
run_remote(10000)
print('Comparison of sequence size of 100000')
run_local(100000)
run_remote(100000)
ray.shutdown()
