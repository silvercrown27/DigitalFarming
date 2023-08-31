import os
from keras.applications.convnext import preprocess_input
from keras.models import load_model
from keras.utils import img_to_array, load_img

model_path = "C:/Users/USER/Documents/models/plant_disease_detection_model.h5"
model = load_model(model_path)


def preprocess_image(image_path):
    img = load_img(image_path, target_size=(128, 128))
    img_array = img_to_array(img)
    img_array = img_array.reshape((1, 128, 128, 3))
    img_array = preprocess_input(img_array)
    return img_array


test_image_dir = "C:/Users/USER/Documents/datasets/plant disease recognition dataset/Validation/Validation"
class_names = os.listdir(test_image_dir)

for class_name in class_names:
    class_dir = os.path.join(test_image_dir, class_name)
    for image_file in os.listdir(class_dir):
        image_path = os.path.join(class_dir, image_file)
        preprocessed_image = preprocess_image(image_path)

        predictions = model.predict(preprocessed_image)
        predicted_class = "Healthy" if predictions[0][0] < 0.5 else "Diseased"
        confidence = predictions[0][0] if predicted_class == "Diseased" else 1 - predictions[0][0]

        print("Image:", image_file)
        print("Predicted class:", predicted_class)
        print("Confidence:", confidence)
        print("--------------------------------------")

