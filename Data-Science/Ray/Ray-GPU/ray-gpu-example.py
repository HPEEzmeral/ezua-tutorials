import tensorflow as tf
import numpy as np

def main():
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    if tf.config.list_physical_devices('GPU'):
        print("TensorFlow will run on GPU.")
    else:
        print("TensorFlow will run on CPU. Make sure your setup allows GPU usage.")

    tf.debugging.set_log_device_placement(True)

    # Creating a larger array of numbers
    data = np.arange(1, 100000)
    tensor = tf.constant(data, dtype=tf.float32)
    
    with tf.device('/GPU:0'):  
        squared_tensor = tf.square(tensor)
    
    print("Original data sample:", data[:10])
    print("Squared data sample:", squared_tensor.numpy()[:10])

if __name__ == "__main__":
    main()
