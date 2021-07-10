from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from streakify.users.serializers import UserSerializer, UserUpdateSerializer
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
		serializer = UserUpdateSerializer( request.user, data=request.data, partial=True)
		try:
			serializer.is_valid(raise_exception=True)
		except:
			return Response({ "detail":"Invalid data" }, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		return Response({
			"body": {
				"name": serializer.data["name"],
				"email": serializer.data["email"],
				"profile_pic": request.user.user_profile.profile_pic if request.user.user_profile.profile_pic else None  
			},
			"detail":"User updated successfully"
		})


class TestView(APIView):
	def get(self,request):
		return Response({"Backend working fine"})
