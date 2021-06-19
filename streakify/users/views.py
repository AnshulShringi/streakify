from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from streakify.users.models import User, UserProfile
from streakify.users.serializers import UserSerializer, UserUpdateSerializer
from rest_framework import serializers, status


class UserProfileView(APIView):

	def get(self, request, *args, **kwargs):
		instance = request.user
		serializer = UserSerializer(instance)
		return Response({
			"body": serializer.data,
			"detail":"User retrieved successfully"
		})

	def patch(self, request, *args, **kwargs):
		profile_pic = request.data.pop("profile_pic") if "profile_pic" in request.data else None
		profile = None
		if profile_pic:
			profile = UserProfile.objects.filter(user=request.user)
			if profile.exists():
				profile[0].profile_pic = profile_pic
				profile[0].save()
		serializer = UserUpdateSerializer( request.user, data=request.data, partial=True)
		try:
			serializer.is_valid(raise_exception=True)
		except:
			return Response({ "detail":"Invalid data" }, status=status.HTTP_400_BAD_REQUEST)
		return Response({
			"body": {
				"name": serializer.data["name"],
				"email": serializer.data["email"],
				"profile_pic": profile[0].profile_pic if profile else "" 
			},
			"detail":"User updated successfully"
		})


class TestView(APIView):
	def get(self,request):
		return Response({"Backend working fine"})
