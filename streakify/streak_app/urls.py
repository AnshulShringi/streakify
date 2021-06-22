from django.urls import path
from streakify.streak_app.views import *


app_name = "streak_app"

urlpatterns = [
    path("streaks", StreakListView.as_view(), name='streak-list'),
    path("streaks/<int:id>", StreakDetailView.as_view(), name='streak-detail'),
]