from django.urls import path
from streakify.streak_app.views import *


app_name = "streak_app"

urlpatterns = [
    path("streaks", StreakListCreateView.as_view(), name='streak-list'),
    path("streaks/<int:id>", StreakDetailView.as_view(), name='streak-detail'),
    path("punch-in/<int:id>", PunchInView.as_view(), name='punch-in-user'),
]