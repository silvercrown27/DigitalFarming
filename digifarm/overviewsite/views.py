import os

from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import AgritectUsers

def landing_page(request):
    return render(request, "index.html")


def learn_page(request):
    return render(request, "learn.html")


def services_page(request):
    return render(request, "services.html")


def about_us_page(request):
    return render(request, "about_us.html")


def signin(request):
    return render(request, "registration.html")


def signup(request):
    return render(request, "registration.html")


def dashboard(request):
    return render(request, "dashboard.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        if User.objects.filter(email=email).exists():
            error_message = "Email already exists. Please use a different email."
            return render(request, 'registration.html', {'error_message': error_message})

        try:
            print("signing in user")
            user = User.objects.create_user(username=username, email=email, password=password)
            AgritectUsers.objects.create(
                user=user, email=email, firstname=firstname, lastname=lastname,
                address1=address1, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone
            ).save()
            print(user.id)

            signin_url = reverse('siteoverview:signin')
            return redirect(signin_url)
        except IntegrityError:
            error_message = "An error occurred during registration. Please try again."
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=email, password=password)
            customer = AgritectUsers.objects.get(user=user)
            if user is not None:
                auth_login(request, user)
                customer_url = reverse('')
                return redirect(customer_url)
            else:
                return JsonResponse({'error': 'Incorrect Email or Password'}, status=400)
        except AgritectUsers.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return render(request, 'signup.html')


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
