import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


def landing_page(request):
    return render(request, "index.html")


def learn_page(request):
    return render(request, "learn.html")


def services_page(request):
    return render(request, "services.html")


def about_us_page(request):
    return render(request, "about_us.html")


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

        context = predict_data(file_path)
        data.update(context)

    return render(request, 'dashboard.html', data)


def predict_data(img):
    import numpy as np
    from keras.models import load_model
    from keras.applications.convnext import preprocess_input
    from keras.preprocessing.image import load_img, img_to_array

    class_labels = ['algal leaf in tea', 'anthracnose in tea', 'Apple Apple scab', 'Apple Black rot', 'Apple Cedar apple rust', 'Apple healthy', 'Bacterial leaf blight in rice leaf', 'bird eye spot in tea', 'Blight in corn Leaf', 'Blueberry healthy', 'brown blight in tea', 'Brown spot in rice leaf', 'cabbage looper', 'Cercospora leaf spot', 'Cherry (including sour) Powdery mildew', 'Cherry (including_sour) healthy', 'Common Rust in corn Leaf', 'Corn (maize) healthy', 'corn crop', 'Garlic', 'ginger', 'Grape Black rot', 'Grape Esca Black Measles', 'Grape healthy', 'Grape Leaf blight Isariopsis Leaf Spot', 'Gray Leaf Spot in corn Leaf', 'healthy tea leaf', 'Leaf smut in rice leaf', 'lemon canker', 'Nitrogen deficiency in plant', 'onion', 'Orange Haunglongbing Citrus greening', 'Peach healthy', 'Pepper bell Bacterial spot', 'Pepper bell healthy', 'potassium deficiency in plant', 'potato crop', 'Potato Early blight', 'Potato healthy', 'potato hollow heart', 'Potato Late blight', 'Raspberry healthy', 'red leaf spot in tea', 'Sogatella rice', 'Soybean healthy', 'Strawberry healthy', 'Strawberry Leaf scorch', 'Tomato Bacterial spot', 'tomato canker', 'Tomato Early blight', 'Tomato healthy', 'Tomato Late blight', 'Tomato Leaf Mold', 'Tomato Septoria leaf spot', 'Tomato Spider mites Two spotted spider mite', 'Tomato Target Spot', 'Tomato Tomato mosaic virus', 'Waterlogging in plant']

    model_path = os.path.join(settings.MEDIA_ROOT, "pdd_model.h5")
    loaded_model = load_model(model_path)

    def preprocess_image(img):
        img = load_img(img, target_size=(128, 128))
        img_array = img_to_array(img)
        img_array = img_array.reshape((1, 128, 128, 3))
        img_array = preprocess_input(img_array)
        return img_array

    test_image_path = img

    preprocessed_image = preprocess_image(test_image_path)

    predictions = loaded_model.predict(preprocessed_image)
    predicted_class_index = np.argmax(predictions[0])
    predicted_class = class_labels[predicted_class_index]

    context = {'classification': predicted_class, "image_path": img.split("/")[-1]}

    print("Predicted class index:", predicted_class_index)
    print("Predicted class:", predicted_class)

    return context
