from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('learn/', views.learn_page, name="learn more"),
    path('upload_pic/', views.update_pic, name="upload pic"),
]
