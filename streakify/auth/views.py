# Core Django Imports
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Local Imports
from streakify.users.models import User

from .decorator import token_retrieve_possible


@method_decorator(token_retrieve_possible, "post")
class GetTokenView(APIView):
    permission_classes = [AllowAny]

    def get_token_object(user_instance):
        token_obj = RefreshToken.for_user(user_instance)
        return {
            "refresh_token": str(token_obj),
            "access_token": str(token_obj.access_token),
        }

    def post(self, request):
        # Get user data
        user_data = {}
        user_data["country_code"] = request.data.get("country_code")
        user_data["mobile_number"] = request.data.get("mobile_number")
        user_data["username"] = user_data["country_code"] + user_data["mobile_number"]

        # Retrieve user intance if exists else create a new one
        user, created = User.objects.get_or_create(**user_data)

        # Get token object(acccess-token, refresh-token) for requesting user
        result = self.get_token_object(user)
        return Response(result)
