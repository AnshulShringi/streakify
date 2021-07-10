from django.urls import path 
from streakify.core.views import ImageUploadView


app_name = "streakify.core"
urlpatterns = [
    path("upload-image", ImageUploadView.as_view(), name="upload-images"),
]
