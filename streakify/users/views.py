from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView


class TestView(APIView):
	def get(self,request):
		return Response({"Backend working fine"})
