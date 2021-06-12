from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from firebase_admin import auth

User = get_user_model()


class GetTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        token = request.data.get("firebase_token") if "firebase_token" in request.data else None
        mobile_number = request.data.get("mobile_number") if "mobile_number" in request.data else None
        country_code = request.data.get("country_code") if "country_code" in request.data else None
        status = "success"
        message = "User verified successfully !"
        body = {}

        if token and mobile_number and country_code:
            phone = country_code + mobile_number
            user = None
            try:
                firebase_user = auth.verify_id_token(token)
                user = User.objects.get(phone=firebase_user["phone_number"])
            except User.DoesNotExist:
                user = User.objects.create(mobile_number=mobile_number,
                                           country_code=country_code)
                user.save()
            except:
                status = "error"
                message = "Firebase Token expired !" 
            if user:
                refresh_token = RefreshToken.for_user(user)
                body["refresh_token"] = str(refresh_token)
                body["access_token"] = str(refresh_token.access_token)

        else:
            status = "error"
            message = "token, mobile_number and country_code required !"
        
        return Response({
            "status": status,
            "body": body,
            "message": message
        })
