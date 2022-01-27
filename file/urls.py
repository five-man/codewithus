from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'file'

urlpatterns = [
    path('file/', views.uploadFile, name='file_upload'),
]+ static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)