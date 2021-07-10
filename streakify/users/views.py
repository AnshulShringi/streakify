from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from streakify.users.serializers import UserSerializer
from rest_framework import status


class UserProfileView(APIView):
	def get(self, request, *args, **kwargs):
		instance = request.user
		serializer = UserSerializer(instance)
		return Response({
			"body": serializer.data,
			"detail":"User retrieved successfully"
		})

	def patch(self, request, *args, **kwargs):
		profile_pic = request.data.get('profile_pic')
		serializer = UserSerializer( request.user, data=request.data, partial=True)
		if serializer.is_valid():
			if profile_pic:
				profile = request.user.user_profile
				profile.profile_pic = profile_pic
				profile.save()
			serializer.save()
			return Response({
				"body": serializer.data,
				"detail":"User updated successfully"
			})
		return Response({ "detail": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


class TestView(APIView):
	def get(self,request):
		return Response({"Backend working fine"})
