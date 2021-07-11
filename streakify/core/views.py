from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from streakify.core.serializers import ImageUploadSerializer
from rest_framework import generics
import environ


env = environ.Env()

class ImageUploadView(generics.CreateAPIView):
    serializer_class = ImageUploadSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()    
            return Response({
                "body": serializer.data,
                "detail":"Image uploaded successfully"
            })
        return Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCheckerView(APIView):
    def post(self, request, *args, **kwargs):
        data = {}
        version_code = request.data.get("version_code", 0)
        current_version = env("VERSION", default=0)
        data["update_type"] = env("UPDATE_TYPE", default=1)
        data["action_url"] = env("ACTION_URL", default="")
        data["update_available"] = True
        
        if version_code and version_code == current_version:
            data["update_available"] = False 
        
        return Response({
            "detail": "Fetched successfully",
            "body": data
        })