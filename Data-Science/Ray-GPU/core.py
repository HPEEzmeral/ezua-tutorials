import tensorflow as tf

def main():
    for iter in range(1, 5):
        # Confirm that TensorFlow is using the GPU.
        print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

        # If GPU is available and accessible for TF, resulting list should not be empty
        tf.config.list_physical_devices('GPU')

        # Enabling logging device placement to find out which devices TF operations and tensors are assigned to
        tf.debugging.set_log_device_placement(True)

        # Create some tensors
        a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
        c = tf.matmul(a, b)

        # The cell above should print an indication that the MatMul op was executed on GPU:0
        print("RAY FRAMEWORK: GPU RESULT", c)

if __name__ == "__main__":
    main()

