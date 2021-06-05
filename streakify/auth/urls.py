# Django imports
from django.urls import path

# Local imports
from streakify.auth.views import *


app_name = "auth"

urlpatterns = [
    path("get-otp/", view=GetOtpView.as_view(), name="get_otp"),
    path("verify-otp/", view=VerifyOtpView.as_view(), name="verify_otp"),
]