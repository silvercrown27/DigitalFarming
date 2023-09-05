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
    path('signin/', views.login, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('submit/', views.submit, name="submit"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
