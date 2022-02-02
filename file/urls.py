from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'file'

urlpatterns = [
    path('file/', views.uploadFile, name='file_upload'),
    path('download/', views.download, name='file_download'),
    path('delete/', views.delete, name='file_delete'),
]+ static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)