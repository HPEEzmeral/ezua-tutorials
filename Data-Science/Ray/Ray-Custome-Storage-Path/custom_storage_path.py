import ray
import os
from concurrent.futures import ThreadPoolExecutor

# Defined the function that calculates the sum of squares
def calculate_sum_of_squares(n):
    return sum(i * i for i in range(1, n+1))


# Function to distribute the computation and write results
def distributed_task(worker_id, n, shared_storage_path):
    result = calculate_sum_of_squares(n)
    result_file = os.path.join(shared_storage_path, f"result_{worker_id}.txt")
    print("result-value:", result,"||", "result-file-path:", result_file)
    with open(result_file, "w") as f:
        f.write(str(result))
    return result_file


def main():
    # Shared storage path
    shared_storage_path = "./custompath/"
    result_file=""

    # Number of workers to use
    num_loops = 10
    total_sum = 0
        
    # Number to calculate sum of squares up to
    N = 100

    # Launch distributed tasks using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_loops) as executor:
        task_futures = [executor.submit(distributed_task, i, N, shared_storage_path) for i in range(num_loops)]
    
    # Get results
    results = [future.result() for future in task_futures]
    # print(results)
    
    for i in range(0, int(len(results))):
        with open(results[i], "r") as f:
            total_sum += int(f.read())
            
    print("Total sum of squares:", total_sum)
    
if __name__=="__main__":
    main()
    print("THE CUSTOM FILE PATH JOB END")