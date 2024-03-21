import numpy as np
import sys
import time

def matrix_multiplication(n,m,p):
    # Generate random matrices
    matrix1 = np.random.rand(n, m)
    matrix2 = np.random.rand(m, p)

    result_matrix = np.dot(matrix1, matrix2)
    return result_matrix

if __name__ == "__main__":
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    p = int(sys.argv[3])

    start_time = time.time()
    result = matrix_multiplication(n,m,p)
    end_time = time.time()
    # Calculate runtime
    runtime = end_time - start_time

    print(result)
    print("Matrix multiplication runtime:", runtime, "seconds")


