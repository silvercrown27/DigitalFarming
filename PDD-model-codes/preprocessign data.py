import warnings, os

import numpy as np
import pandas as pd
import tensorflow as tf

import keras
from keras import layers
from keras.models import load_model

import matplotlib.pyplot as plt
from custom_functions import custom_image_dataset_from_dir_pdd


def create_dataset(file_path):
    data = []
    for root, directories, files in os.walk(file_path):
        dir_name = root.split('/')[-1]
        for file in files:
            file_path = os.path.join(dir_name, file)
            data.append([file_path, dir_name])
    return data


def convert_to_float(image, label):
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    label = tf.cast(label, dtype=tf.float32)
    return image, label


def set_seed(seed=19893):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    os.environ["TF_DETERMINISTIC_OPS"] = "1"


set_seed()
plt.rc("figure", autolayout=True)
plt.rc("axes", labelweight="bold", labelsize="large", titleweight="bold", titlesize=16, titlepad=10)
plt.rc("image", cmap="magma")
warnings.filterwarnings("ignore")
AUTOTUNE = tf.data.experimental.AUTOTUNE

image_paths = "C:/Users/USER/Documents/datasets/plant disease datasets/Image Data base/Image Data base/"
pre_trained_model = 'C:/Users/USER/Documents/models/cv-course-models/cv-course-models/vgg16-pretrained-base'

df = create_dataset(image_paths)
df = np.array(df)

dataset = pd.DataFrame()
dataset['image_path'] = df[:, 0]
dataset['labels'] = df[:, 1]
output_csv = 'pdd_dataset.csv'
dataset.to_csv(output_csv, index=False)

data, label_mapping_df = custom_image_dataset_from_dir_pdd('pdd_dataset.csv', image_paths)
ds_train = (data.map(convert_to_float).prefetch(buffer_size=AUTOTUNE))

pre_trained_base = load_model(pre_trained_model)
pre_trained_base.trainable = False

model = keras.Sequential([
    pre_trained_base,

    layers.RandomRotation('horizontal'),
    layers.RandomContrast(0.5),
    layers.RandomTranslation(),
    layers.Conv2D(filters=64, kernel_size=5, activation='relu', padding='same', input_shape=[128, 128, 3]),
    layers.MaxPool2D(),

    layers.Conv2D(filters=128, kernel_size=3, activation="relu", padding='same'),
    layers.MaxPool2D(),

    layers.Conv2D(filters=128, kernel_size=3, activation="relu", padding='same'),
    layers.MaxPool2D(),

    layers.Flatten(),
    layers.Dense(units=6, activation="relu"),
    layers.Dense(units=len(label_mapping_df), activation="softmax"),  # Use softmax for multi-class classification
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
history = model.fit(ds_train, epochs=30, verbose=2)

# Convert encoded labels back to original categorical values
# encoded_labels = np.arange(len(label_mapping_df))
# decoded_labels = label_mapping_df['Categorical_Value'].values
# Assuming you have some test data
# test_predictions = model.predict(test_data)  # Replace with your test data
#
# # Convert predicted encoded labels to original categorical values
# predicted_labels = np.argmax(test_predictions, axis=1)
# predicted_categorical_labels = [decoded_labels[pred_label] for pred_label in predicted_labels]

decoded_output_csv = 'decoded_values.csv'
label_mapping_df.to_csv(decoded_output_csv, index=False)

model.save('plant_disease_detection_model-v1.h5')
