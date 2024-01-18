import numpy as np
import time

import warnings
warnings.filterwarnings('ignore') 

Stime = time.perf_counter()

def perform_cpu_task():
    try:
        # Perform metric multiplication on the CPU using NumPy
        a = np.array([[1, 2], [3, 4]], dtype=np.float32)
        b = np.array([[5, 6], [7, 8]], dtype=np.float32)
        result = np.matmul(a, b)
        return result
    except Exception as e:
        print(f"Error in CPU task: {e}")
        return None
    
def create_matrix(size):
    return np.random.normal(size=size)

def multiply_matrices(x, y):
    return np.dot(x, y)

def sum_matrices(x, y):
    return np.add(x, y)

print(f"Finished in {time.perf_counter()-Stime:.2f}")

def main():
    try:
        # Call the functions
        m1 = create_matrix([10000, 10000])
        m2 = create_matrix([10000, 10000])
        m3 = create_matrix([10000, 10000])
        m4 = create_matrix([10000, 10000])

        m12 = multiply_matrices(m1, m2)
        m34 = multiply_matrices(m3, m4)

        a12_34 =  sum_matrices(m12, m34)

        ## Results
        MM = a12_34
        result = perform_cpu_task()
        
        if result is not None:
            print("Metric Multiplication Result on CPU:")
            print(result)
            print(MM)
            print("RESULT:", result)
            return result
        else:
            print("Error: CPU task failed.")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()
