import matplotlib.pyplot as plt
import os, warnings
import pandas as pd
import numpy as np

import keras
from keras import layers
import tensorflow as tf
from keras.utils import image_dataset_from_directory as idf


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


pre_trained_model = 'C:/Users/USER/Documents/models/cv-course-models/cv-course-models/vgg16-pretrained-base'
train_data_path = "C:/Users/USER/Documents/datasets/plant disease recognition dataset/Train/Train/plants.csv"
train_image_path = "C:/Users/USER/Documents/datasets/plant disease recognition dataset/Train/Train/"
test_data_path = "C:/Users/USER/Documents/datasets/plant disease recognition dataset/Train/Train/plants.csv"
test_image_path = "C:/Users/USER/Documents/datasets/plant disease recognition dataset/Train/Train"


train_ = idf(train_image_path, shuffle=True, batch_size=128, interpolation="nearest", seed=101, image_size=(128, 128))
valid_ = idf(test_image_path, shuffle=True, batch_size=128, interpolation="nearest", seed=101, image_size=(128, 128))

train_ = (train_.map(convert_to_float).cache().prefetch(buffer_size=AUTOTUNE))
valid_ = (valid_.map(convert_to_float).cache().prefetch(buffer_size=AUTOTUNE))

pretrained_base = keras.models.load_model(pre_trained_model)
pretrained_base.trainable = False

model = keras.Sequential([
    pretrained_base,
    layers.Conv2D(filters=64, kernel_size=3, activation='relu', padding='same', input_shape=[128, 128, 3]),
    layers.MaxPool2D(),

    layers.Conv2D(filters=128, kernel_size=3, activation="relu", padding='same'),
    layers.MaxPool2D(),

    layers.Flatten(),
    layers.Dense(units=64, activation="relu"),
    layers.Dense(units=3, activation="softmax"),
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

history = model.fit(train_, validation_data=valid_, epochs=10, verbose=2)
print("Done training of model...")


save_dir = "C:/Users/USER/Documents/models"
os.makedirs(save_dir, exist_ok=True)
model.save(os.path.join(save_dir, "plant_disease_detection_model.h5"))
plt.show()
