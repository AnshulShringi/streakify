# Django imports
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 

# Local imports
from streakify.users.views import *


app_name = "users"
urlpatterns = [
    path("get-token/", GetTokenView.as_view(), name='token_obtain'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path("update-user-profile/", view=UpdateUserProfile.as_view(), name="update-user-profile"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
