from django.urls import path
from streakify.friends.views import *

app_name = "friends"

urlpatterns = [
    path("friends", FriendsAPIView.as_view(), name='my-friends'),
    path("update-request-status/<int:id>", FriendRequestUpdateView.as_view(), name='update-request-status'),
]