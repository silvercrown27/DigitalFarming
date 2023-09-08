from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

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
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            customer = AgritectUsers.objects.get(user=user)
            if user is not None:
                auth_login(request, user)
                customer_url = reverse('usersite:dashboard')
                return redirect(customer_url)
            else:
                return JsonResponse({'error': 'Incorrect Email or Password'}, status=400)
        except AgritectUsers.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return render(request, 'registration.html')


