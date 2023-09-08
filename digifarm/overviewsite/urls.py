from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "siteoverview"

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('learn/', views.learn_page, name="learn-more"),
    path('services/', views.services_page, name="services"),
    path('about-us/', views.about_us_page, name="about"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
