import importlib
import subprocess
# Check if mlflow is installed
try:
    importlib.import_module('mlflow')
except ImportError:
    # If mlflow is not installed, install it with pip
    subprocess.check_call(["pip", "install", "mlflow"])
import numpy as np
import pandas as pd
from pathlib import Path
import os.path
import matplotlib.pyplot as plt
import tensorflow as tf
import mlflow
import mlflow.tensorflow
import os
import urllib3
import time


# Create a list with the filepaths for training and testing
train_dir = Path('/mnt/c/Users/dderichswei/Downloads/end2end/train/')
train_filepaths = [p for p in train_dir.glob('**/*.jpg') if not p.name.startswith('.')] # ignore .ipynb files and directories

test_dir = Path('/mnt/c/Users/dderichswei/Downloads/end2end/test/')
test_filepaths = [p for p in test_dir.glob('**/*.jpg') if not p.name.startswith('.')]

val_dir = Path('/mnt/c/Users/dderichswei/Downloads/end2end/validation/')
val_filepaths = [p for p in val_dir.glob('**/*.jpg') if not p.name.startswith('.')]

def proc_img(filepath):
    """ Create a DataFrame with the filepath and the labels of the pictures
    """

    labels = [str(filepath[i]).split("/")[-2] \
              for i in range(len(filepath))]

    filepath = pd.Series(filepath, name='Filepath',dtype=str)
    labels = pd.Series(labels, name='Label',dtype=str)

    # Concatenate filepaths and labels
    df = pd.concat([filepath, labels], axis=1)

    # Shuffle the DataFrame and reset index
    df = df.sample(frac=1).reset_index(drop = True)
    
    return df

train_df = proc_img(train_filepaths)
test_df = proc_img(test_filepaths)
val_df = proc_img(val_filepaths)

print('-- Training set --\n')
print(f'Number of pictures: {train_df.shape[0]}\n')
print(f'Number of different labels: {len(train_df.Label.unique())}\n')
print(f'Labels: {train_df.Label.unique()}')

print('-- Test set --\n')
print(f'Number of pictures: {test_df.shape[0]}\n')
print(f'Number of different labels: {len(test_df.Label.unique())}\n')
print(f'Labels: {test_df.Label.unique()}')

print('-- Validate set --\n')
print(f'Number of pictures: {val_df.shape[0]}\n')
print(f'Number of different labels: {len(val_df.Label.unique())}\n')
print(f'Labels: {val_df.Label.unique()}')

# Create a DataFrame with one Label of each category
df_unique = train_df.copy().drop_duplicates(subset=["Label"]).reset_index()

# Display some pictures of the dataset
fig, axes = plt.subplots(nrows=6, ncols=6, figsize=(15, 10),
                        subplot_kw={'xticks': [], 'yticks': []})

for i, ax in enumerate(axes.flat):
    if i < len(df_unique):
        ax.imshow(plt.imread(df_unique.iloc[i]['Filepath']))
        ax.set_title(df_unique.iloc[i]['Label'], fontsize = 12)
plt.tight_layout(pad=0.5)
#plt.show()


# Create an image data generator for preprocessing train images using MobileNetV2
train_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
)

# Generate a flow of images and labels from a Pandas dataframe for training
train_images = train_generator.flow_from_dataframe(
    dataframe=train_df, # Use the specified Pandas dataframe
    x_col='Filepath', # Use the 'Filepath' column as the input (x) data
    y_col='Label', # Use the 'Label' column as the output (y) data
    target_size=(224, 224), # Resize the images to the specified dimensions
    color_mode='rgb', # Use RGB color mode
    class_mode='categorical', # Use categorical classification
    batch_size=32, # Generate batches of 32 images at a time
    shuffle=True, # Shuffle the order of the images
    seed=0, # Use a fixed seed for reproducibility
    rotation_range=30, # Randomly rotate images up to 30 degrees
    zoom_range=0.15, # Randomly zoom images up to 15%
    width_shift_range=0.2, # Randomly shift images horizontally up to 20%
    height_shift_range=0.2, # Randomly shift images vertically up to 20%
    shear_range=0.15, # Randomly apply shearing transformations to images
    horizontal_flip=True, # Randomly flip images horizontally
    fill_mode="nearest", # Use the nearest pixel to fill any empty spaces created by image transformations
)

# Create an image data generator for preprocessing validation images using MobileNetV2
val_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
)

# Generate a flow of images and labels from a Pandas dataframe for validation
val_images = val_generator.flow_from_dataframe(
    dataframe=val_df, # Use the specified Pandas dataframe
    x_col='Filepath', # Use the 'Filepath' column as the input (x) data
    y_col='Label', # Use the 'Label' column as the output (y) data
    target_size=(224, 224), # Resize the images to the specified dimensions
    color_mode='rgb', # Use RGB color mode
    class_mode='categorical', # Use categorical classification
    batch_size=32, # Generate batches of 32 images at a time
    shuffle=True, # Shuffle the order of the images
    seed=0, # Use a fixed seed for reproducibility
    rotation_range=30, # Randomly rotate images up to 30 degrees
    zoom_range=0.15, # Randomly zoom images up to 15%
    width_shift_range=0.2, # Randomly shift images horizontally up to 20%
    height_shift_range=0.2, # Randomly shift images vertically up to 20%
    shear_range=0.15, # Randomly apply shearing transformations to images
    horizontal_flip=True, # Randomly flip images horizontally
    fill_mode="nearest" # Use the nearest pixel to fill any empty spaces created by image transformations
)

# Create an image data generator for preprocessing test images using MobileNetV2
test_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input
)

# Generate a flow of images and labels from a Pandas dataframe
test_images = test_generator.flow_from_dataframe(
    dataframe=test_df, # Use the specified Pandas dataframe
    x_col='Filepath', # Use the 'Filepath' column as the input (x) data
    y_col='Label', # Use the 'Label' column as the output (y) data
    target_size=(224, 224), # Resize the images to the specified dimensions
    color_mode='rgb', # Use RGB color mode
    class_mode='categorical', # Use categorical classification
    batch_size=32, # Generate batches of 32 images at a time
    shuffle=False # Do not shuffle the order of the images
)

# Load the pretained model
urllib3.disable_warnings()
pretrained_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet',
    pooling='avg'
)
pretrained_model.trainable = False

param_epoch = 20
param_batch_size = 36
param_patience = 2

inputs = pretrained_model.input
urllib3.disable_warnings()
x = tf.keras.layers.Dense(128, activation='relu')(pretrained_model.output)
x = tf.keras.layers.Dense(128, activation='relu')(x)

outputs = tf.keras.layers.Dense(37, activation='softmax')(x)

model = tf.keras.Model(inputs=inputs, outputs=outputs)

# Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model
history = model.fit(
    train_images,
    validation_data=val_images,
    batch_size = param_batch_size,
    epochs=param_epoch,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=param_patience,
            restore_best_weights=True
        )
    ]
)

model.save('end2end.h5')