from django.urls import path
from imagedetection import views
urlpatterns = [
    path('upload/',views.UploadImage, name='upload'),
    path('capture-frames/',views.Captureframes,name='capture-frames'),
]
