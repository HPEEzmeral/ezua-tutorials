import sys
import os
import time

# The functions in this section will allow us to compare how long it takes to generate multiple long Fibonacci sequences both locally and in parallel.

def fibonacci_function(sequence_size):
    fibonacci = []
    for i in range(0, sequence_size):
        if i < 2:
            fibonacci.append(i)
            continue
        fibonacci.append(fibonacci[i - 1] + fibonacci[i - 2])
    return sequence_size

if __name__ == "__main__":
    n = int(sys.argv[1])
    start_time = time.time()
    [fibonacci_function(n) for _ in range(os.cpu_count())]
    end_time = time.time()
    duration = end_time - start_time
    print(f"Computation time for {n} sequence is {duration}")
