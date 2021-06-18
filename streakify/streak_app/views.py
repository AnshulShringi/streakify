from rest_framework.response import Response
from rest_framework.views import APIView
from streakify.streak_app.models import Streak, StreakRecord
from streakify.streak_app.serializers import StreakCreateSerializer, StreakListSerializer, StreakDetailSerializer
from rest_framework.generics import ListAPIView
from rest_framework import status
from streakify.users.models import *


class StreakListView(ListAPIView):
    queryset = StreakRecord.objects.all()
    serializer_class = StreakListSerializer
    
    def get_queryset(self):
        queryset = self.queryset.filter(participant=self.request.user)
        return queryset.order_by('-created')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({  
            "body":serializer.data, 
            "detail":"Data retrieved successfully" 
        })


class StreakCreateView(APIView):
    queryset = Streak.objects.all()
    serializer_class = StreakCreateSerializer
    
    def post(self, request, *args, **kwargs):
        user_ids = request.data.pop("user_ids") if "user_ids" in request.data else None
        user_ids = user_ids.split(",") if user_ids else []
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({ "detail":"Invalid data" }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "body": serializer.validated_data,
            "detail":"Streak created successfully"
        }, status=status.HTTP_201_CREATED)


class StreakDetailView(APIView):
    queryset = Streak.objects.all()
    serializer_class = StreakDetailSerializer
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "body": serializer.data,
            "detail":"Streak details retrieved successfully"
        })

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer( instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({ "detail":"Invalid data" }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "body": serializer.data,
            "detail":"Streak updated successfully"
        })

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "detail":"Streak deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)