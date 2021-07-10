from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from streakify.core.serializers import ImageUploadSerializer
from rest_framework import generics


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