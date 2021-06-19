from django.urls import path 
from streakify.users.views import *


app_name = "users"
urlpatterns = [
    path("test", TestView.as_view(), name="test-view"),
    path("profile", UserProfileView.as_view(), name="user-profile"),
]
