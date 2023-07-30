import ray
import numpy as np
import tensorflow as tf

# Please make sure about below points
# 1. If you execute the job from a notebook, then your connection URL should be as below
#    ray.init(address="ray://kuberay-head-svc.kuberay:10001")
# 2. For this example tensorflow package needs to installed, either install it manually or pass the installation command in init command as below
#    ray.init(address="ray://kuberay-head-svc.kuberay:10001", runtime_env={"pip": ["tensorflow"]})
# 3. If you have proxy, then you need to add following dictionary into runtime_env parameter in ray.init method
#    "env_vars": {"http_proxy": "<PROXY_ADDRESS>", "https_proxy": "<PROXY_ADDRESS>"}
# ray.init(address="ray://kuberay-head-svc.kuberay:10001", runtime_env={"pip": ["tensorflow"]})

ray.init(address="ray://kuberay-head-svc.kuberay:10001", ignore_reinit_error=True)

@ray.remote(num_gpus=1)
def gpu_operation(data):
    # Perform GPU-accelerated operation
    # Example: Square each element of the input array using TensorFlow
    with tf.device("/GPU:0"):
        tensor = tf.constant(data)
        squared = tf.square(tensor)
        result = squared.numpy()
    return result

# data
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
num_chunks = 2

# Split the data into chunks
data_chunks = np.array_split(data, num_chunks)

# Submit GPU operations for execution in parallel
result_refs = [gpu_operation.remote(chunk) for chunk in data_chunks]

# Retrieve the results
results = ray.get(result_refs)

print(results)
