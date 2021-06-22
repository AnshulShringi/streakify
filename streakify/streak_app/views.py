from rest_framework.response import Response
from rest_framework.views import APIView
from streakify.streak_app.models import Streak, StreakRecord
from streakify.streak_app.serializers import StreakCreateSerializer, StreakRecordSerializer
from rest_framework.generics import ListAPIView
from rest_framework import status
from streakify.users.models import *


class StreakListView(ListAPIView):
    queryset = StreakRecord.objects.all()
    
    def get_queryset(self):
        queryset = self.queryset.filter(participant=self.request.user)
        return queryset.order_by('-created')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = StreakRecordSerializer(queryset, many=True)
        return Response({  
            "body":{
                "streak_records": serializer.data
            }, 
            "detail":"Data retrieved successfully" 
        })

    def post(self, request, *args, **kwargs):
        serializer = StreakCreateSerializer(data=request.data, context={'request':request})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({ "detail":"Invalid data" }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "body": serializer.data,
            "detail":"Streak created successfully"
        }, status=status.HTTP_201_CREATED)


class StreakDetailView(APIView):
    queryset = Streak.objects.all()
    serializer_class = StreakRecordSerializer
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