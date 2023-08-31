import pandas as pd
import os
import cv2
import numpy as np
import tensorflow as tf
import keras
from keras import layers
from sklearn.preprocessing import OrdinalEncoder

INTERPOLATION_DICT = {
    'nearest': cv2.INTER_NEAREST,
    'bilinear': cv2.INTER_LINEAR,
    'bicubic': cv2.INTER_CUBIC,
    'lanczos': cv2.INTER_LANCZOS4
}


def custom_image_dataset_for_pdd_model(train_csv, train_path, test_csv, test_path, image_size=(128, 128),
                                      interpolation='nearest', batch_size=192, shuffle=True):
    print("Beginning Preprocessing Images...")
    train_data = pd.read_csv(train_csv)
    train_data = train_data.sample(frac=1.0, random_state=42)
    test_data = pd.read_csv(test_csv)
    test_data = test_data.sample(frac=1.0, random_state=42)

    train_images = train_data['image'].values
    train_labels = train_data["labels"].values
    test_images = test_data["image"].values
    test_labels = test_data["labels"].values

    encoder = OrdinalEncoder()
    unique_values = np.unique(train_labels)
    encoder.fit(unique_values.reshape(-1, 1))

    encoded_labels_train = encoder.transform(train_labels.reshape(-1, 1)).astype("float32")
    encoded_labels_test = encoder.transform(test_labels.reshape(-1, 1)).astype("float32")

    print("Length of unique_values:", len(unique_values))
    print("Length of encoded_labels_train:", len(encoded_labels_train))
    print("Length of encoded_labels_test:", len(encoded_labels_test))

    label_mapping_df = pd.DataFrame(
        {'Categorical_Value': unique_values, 'Encoded_Value': encoder.transform(unique_values.reshape(-1, 1))[:, 0]})

    training_image_paths = [os.path.join(train_path, name) for name in train_images]
    testing_image_paths = [os.path.join(test_path, name) for name in test_images]

    tr_images = []
    ts_images = []

    for img_path in training_image_paths:
        img = cv2.imread(img_path)
        img = cv2.resize(img, image_size, interpolation=INTERPOLATION_DICT[interpolation])
        tr_images.append(img)

    for img_path in testing_image_paths:
        img = cv2.imread(img_path)
        img = cv2.resize(img, image_size, interpolation=INTERPOLATION_DICT[interpolation])
        ts_images.append(img)

    tr_images = np.array(tr_images, dtype=np.float32) / 255.0
    ts_images = np.array(ts_images, dtype=np.float32) / 255.0

    X_train, y_train = tr_images, encoded_labels_train
    X_test, y_test = ts_images, encoded_labels_test

    data_augmentation = keras.Sequential([
        layers.RandomRotation(factor=0.15),
        layers.RandomTranslation(height_factor=0.1, width_factor=0.1),
        layers.RandomContrast(0.5),
        layers.Rescaling(1. / 255)
    ])

    X_train = data_augmentation(X_train)
    X_test = data_augmentation(X_test)

    train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train))
    test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test))

    if shuffle:
        train_dataset = train_dataset.shuffle(len(X_train))
        test_dataset = test_dataset.shuffle(len(X_test))

    train_dataset = train_dataset.batch(batch_size)
    test_dataset = test_dataset.batch(batch_size)

    print("Done Preprocessing Images...")
    return train_dataset, test_dataset, label_mapping_df



def custom_image_dataset_from_dir_pdd(train_csv, train_path, image_size=(128, 128),
                                      interpolation='nearest', batch_size=192, shuffle=True):
    print("Beginning Preprocessing Images...")
    train_data = pd.read_csv(train_csv)
    train_data = train_data.sample(frac=1.0, random_state=42)

    train_images = train_data['image_path'].values
    train_labels = train_data["labels"].values

    encoder = OrdinalEncoder()
    unique_values = np.unique(train_labels)
    encoder.fit(unique_values.reshape(-1, 1))

    encoded_labels = encoder.transform(train_labels.reshape(-1, 1)).astype("float32")

    print("Length of unique_values:", len(unique_values))
    print("Length of encoded_labels:", len(encoded_labels))
    label_mapping_df = pd.DataFrame({'Categorical_Value': unique_values, 'Encoded_Value': encoder.transform(unique_values.reshape(-1, 1))[:, 0]})

    training_image_paths = [os.path.join(train_path, name) for name in train_images]

    tr_images = []

    for img_path in training_image_paths:
        img = cv2.imread(img_path)
        img = cv2.resize(img, image_size, interpolation=INTERPOLATION_DICT[interpolation])
        tr_images.append(img)

    tr_images = np.array(tr_images, dtype=np.float32) / 255.0

    X, y = tr_images, encoded_labels

    train_dataset = tf.data.Dataset.from_tensor_slices((X, y))

    if shuffle:
        train_dataset = train_dataset.shuffle(len(X))

    train_dataset = train_dataset.batch(batch_size)

    print("Done Preprocessing Images...")
    return train_dataset, label_mapping_df
