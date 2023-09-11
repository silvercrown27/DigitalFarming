import json
import os

from django.contrib.auth import logout
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from overviewsite.models import AgritectUsers
from .models import *


@login_required(login_url='/overview/')
def home_page(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    context = {}
    return render(request, 'dashboard.html', context)


def myspace_page(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    return render(request, "mySpace.html")


def calculate_drive_size(drive_id):
    total_size = Files.objects.filter(drive_id=drive_id).aggregate(Sum('file_size'))['file_size__sum']
    return total_size if total_size else 0


def new_drive(drive_name, user_name, capacity):
    drive_user = AgritectUsers.objects.get(username=user_name)

    if capacity <= AgritectUsers.object.get(username=user_name).allocated_space:
        Drives.objects.create(drive_name=drive_name, drive_user=drive_user, capacity=capacity)
        print(f"New drive {drive_name} created successfully!")
    else:
        print(f"The capacity ({capacity}) exceeds the allocated space for user {user_name}"
              f" ({drive_user.allocated_space}).")


def exists(model, drive_id, path):
    try:
        md = model.objects.filter(drive_id=drive_id, path=path)
        return True

    except md.DoesNotExist:
        return False


def add_folder(name, path, drive_id):
    Folders.objects.create(name=name, path=path, drive_id=drive_id)


def add_file(name, path, ext, folder_id, drive_id, size):
    if calculate_drive_size(drive_id) > size:
        Files.objects.create(name=name, path=path, file_ext=ext, folder_id=folder_id, drive_id=drive_id, file_size=size)


def get_size(filepath):
    with open(filepath, 'rb') as f:
        size = len(f) / (1024 ** 2)
        return size


def add_file_info_to_db(folder_id, drive_id, file):
    file_name = os.path.splitext(file[0])
    file_size = get_size(file)
    extension = os.path.splitext(file)[1]
    folder_id = folder_id
    drive_id = drive_id
    add_file(file_name, file, extension, folder_id, drive_id, file_size)


def remove_media_root(file_paths):
    media_root = settings.MEDIA_ROOT
    len_mr = len(media_root)

    return file_paths[len_mr + 1:]


def upload(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/overview/')

    try:
        customer = AgritectUsers.objects.get(user=user)

        if customer is not None:
            data = {}
            image_urls = []
            if request.method == 'POST':
                files = request.FILES.getlist('img_upload')

                if len(files) == 0:
                    return JsonResponse({'error': 'No files uploaded'}, status=400)

                default_path = f"{customer.id}/My Desktop"

                fs = FileSystemStorage()

                for file in files:
                    file_path = os.path.join(settings.MEDIA_ROOT, default_path, file.name)
                    fs.save(file_path, file)

                    image_url = os.path.join(settings.MEDIA_URL, default_path, file.name)
                    image_urls.append(image_url)
                    context = predict_data(file_path)
                    data.update(context)

                data['image_url'] = image_urls

            return JsonResponse(data)

    except AgritectUsers.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


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


def logout_user(request):
    logout(request)
    return redirect('/overview/')


def update_ac_details(request, username):
    if request.method == "POST":
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        user = AgritectUsers.objects.get(username=username)

        user.email = email
        user.first_name = firstname
        user.last_name = lastname
        user.address1 = address1
        user.address2 = address2
        user.city = city
        user.state = state
        user.zip_code = zip_code
        user.phone = phone
        user.save()

    return HttpResponseRedirect(reverse("usersite:myspace", ))
