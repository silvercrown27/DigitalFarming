import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.shortcuts import render, redirect
from keras.src.utils import load_img, img_to_array


def landing_page(request):
    return render(request, "index.html")


def learn_page(request):
    return render(request, "learn.html")

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def dashboard(request):
    return render(request, "dashboard.html")


def submit(request):
    data = {}
    if request.method == "POST":
        image = request.FILES.get('img_upload')

        default_path = ""
        fs = FileSystemStorage()
        file_path = os.path.join(settings.MEDIA_ROOT, default_path, image.name)
        fs.save(file_path, image)

        context = predict_data(file_path)  # Call the predict_data function with the full file path
        data.update(context)  # Add the context items to the data dictionary

    return render(request, 'dashboard.html', data)


def predict_data(img):
    import numpy as np
    from keras.models import load_model
    from keras.applications.convnext import preprocess_input
    from keras.preprocessing.image import load_img, img_to_array  # Corrected imports
    from django.conf import settings
    import os

    class_labels = ['Healthy', 'Powdery', 'Rust']
    model_path = os.path.join(settings.MEDIA_ROOT, "plant_disease_detection_model.h5")
    loaded_model = load_model(model_path)

    def preprocess_image(img):
        img = load_img(img, target_size=(128, 128))
        img_array = img_to_array(img)
        img_array = img_array.reshape((1, 128, 128, 3))
        img_array = preprocess_input(img_array)
        return img_array

    test_image_path = img
    input_size = (128, 128)

    preprocessed_image = preprocess_image(test_image_path)

    predictions = loaded_model.predict(preprocessed_image)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class = class_labels[predicted_class_index]

    context = {'classification': predicted_class, "image_path": img.split("/")[-1]}

    print("Predicted class index:", predicted_class_index)
    print("Predicted class:", predicted_class)

    return context
