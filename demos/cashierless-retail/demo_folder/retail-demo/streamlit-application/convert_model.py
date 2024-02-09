import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the .h5 model
model = load_model('./end2end.h5')

# Convert the .h5 model to a .pb file
tf.saved_model.save(model, './end2end.pb')