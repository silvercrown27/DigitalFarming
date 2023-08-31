from django.shortcuts import render


def landing_page(request):
    return render(request, "index.html")


def learn_page(request):
    return render(request, "learn.html")

def login(request):
    return render(request, "login.html")

