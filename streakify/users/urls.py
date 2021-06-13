# Django imports
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 

# Local imports
from streakify.users.views import *


app_name = "users"
urlpatterns = [
    path("test",TestView.as_view()),
    path("get-token/", GetTokenView.as_view(), name='token_obtain'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]
