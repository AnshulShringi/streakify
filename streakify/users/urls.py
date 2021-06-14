from django.urls import path 
from streakify.users.views import *


app_name = "users"
urlpatterns = [
    path("get-token", GetTokenView.as_view(), name='token_obtain'),
    path('refresh-token', RefreshTokenView.as_view(), name='token_refresh'),
]
