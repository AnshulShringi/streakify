from django.urls import path

from streakify.users.views import UserDetailView

app_name = "users"

urlpatterns = [
    path("profile", UserDetailView.as_view(), name="user-detail"),
]
