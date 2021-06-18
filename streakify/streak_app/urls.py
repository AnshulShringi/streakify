from django.urls import path
from streakify.streak_app.views import *


app_name = "streak_app"

urlpatterns = [
    path("streak-list", StreakListView.as_view(), name='streak-list'),
    path("create-streak", StreakCreateView.as_view(), name='create-streak'),
    path("streak-detail/<int:id>", StreakDetailView.as_view(), name='streak-detail'),
]