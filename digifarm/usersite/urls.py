from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "usersite"

urlpatterns = [
    path('', views.home_page, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('submit/', views.submit, name="submit"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
