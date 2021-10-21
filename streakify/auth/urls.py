from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from streakify.auth.views import GetTokenView

app_name = "auth"

urlpatterns = [
    path("get-token", GetTokenView.as_view(), name="token_obtain"),
    path("refresh-token", TokenRefreshView.as_view(), name="token_refresh"),
    # For testing only
    path("test-get-token", TokenObtainPairView.as_view(), name="test-get-token-view"),
]
