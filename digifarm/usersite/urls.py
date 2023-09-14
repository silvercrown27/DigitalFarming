from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "usersite"

urlpatterns = [
    path('', views.home_page, name="home"),
    path('myspace/', views.myspace_page, name="myspace"),
    path('account/', views.myspace_page, name="user-account"),
    path('upload/', views.upload, name="upload_image"),
    path('video_feed/', views.video_feed, name='video_feed'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
