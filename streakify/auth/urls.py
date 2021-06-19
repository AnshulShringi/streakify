from django.urls import path 
from streakify.auth.views import *


app_name = "auth"
urlpatterns = [
    path("get-token", GetTokenView.as_view(), name='token_obtain'),
    path('refresh-token', RefreshTokenView.as_view(), name='token_refresh'),
]
