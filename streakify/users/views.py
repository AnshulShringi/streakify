from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from firebase_admin import auth

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UpdateUserProfile(APIView):
    def patch(self, request):
        content = {'message': 'Hello, GeeksforGeeks'}
        return Response(content)


# Other views

class GetTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        token = request.data.get("token") if "token" in request.data else None
        mobile_number = request.data.get("mobile_number") if "mobile_number" in request.data else None
        country_code = request.data.get("token") if "token" in request.data else None
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
                body["refresh"] = str(refresh_token)
                body["access"] = str(refresh_token.access_token)

        else:
            status = "error"
            message = "token, mobile_number and country_code required !"
        
        return Response({
            "status": status,
            "body": body,
            "message": message
        })
