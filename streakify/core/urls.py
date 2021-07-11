from django.urls import path 
from streakify.core.views import ImageUploadView, UpdateCheckerView


app_name = "streakify.core"
urlpatterns = [
    path("upload-image", ImageUploadView.as_view(), name="upload-images"),
    path("update-checker", UpdateCheckerView.as_view(), name="update-checker"),
]
