from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from firebase_admin import auth
from streakify.core.models import Country
from streakify.users.models import User, UserProfile
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError


class GetTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        firebase_token = request.data.get("firebase_token") if "firebase_token" in request.data else None
        mobile_number = request.data.get("mobile_number") if "mobile_number" in request.data else None
        country_code = request.data.get("country_code") if "country_code" in request.data else None
        body = {}
        if firebase_token and mobile_number and country_code:
            phone = country_code + mobile_number
            try:
                firebase_user = auth.verify_id_token(firebase_token)
            except:
                message = "Firebase token invalid or expired"
                return Response({ "status": "error", "body": body, "message": message})
        
            if phone != firebase_user["phone_number"]:
                message = "country_code or mobile_number doesn't match with firebase account"
                return Response({ "status":"error", "body": body, "message": message})

            country, created = Country.objects.get_or_create(country_code=country_code)
            profile = UserProfile.objects.filter(country=country, mobile_number=mobile_number)
            if profile:
                user = profile[0].user
            else:
                user = User.objects.create(username=phone)
                user.save()
                UserProfile.objects.create(user=user, country=country, mobile_number=mobile_number).save()

            # Generating token for requesting user
            refresh_token = RefreshToken.for_user(user)
            body["refresh_token"] = str(refresh_token)
            body["access_token"] = str(refresh_token.access_token)
            message = "User verified successfully"
            return Response({ "status":"success", "body": body, "message": message})
            
        message = "firebase_token, mobile_number and country_code required"
        return Response({ "status":"error", "body": body, "message": message})


class RefreshTokenView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh = request.data.get("refresh") if "refresh" in request.data else None
        if not refresh:
            return Response({ "status":"error", "body":{}, "message":"refresh token required" })
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response({ "status":"error", "body":{}, "message":"Token invalid or expired" })
        
        return Response({
            "status": "success",
            "body":serializer.validated_data,
            "message":"Token refreshed successfully"
        })


class TestView(APIView):
	def get(self,request):
		print("Test url called")
		return Response({"Working fine"})
