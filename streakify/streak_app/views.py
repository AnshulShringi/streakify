from rest_framework.response import Response
from rest_framework.views import APIView
from streakify.streak_app.models import Streak, StreakRecord
from streakify.streak_app.serializers import StreakCreateSerializer, StreakListSerializer, StreakDetailSerializer
from rest_framework.generics import ListAPIView


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
            "status":"success", 
            "body":serializer.data, 
            "message":"Data retrieved successfully" 
        })


class StreakCreateView(APIView):
    queryset = Streak.objects.all()
    serializer_class = StreakCreateSerializer
    
    def post(self, request, *args, **kwargs):
        friends = request.data.pop("")
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({ "status":"error", "body":{}, "message":"Invalid data" })
        serializer.save()
        return Response({
            "status": "success",
            "body": serializer.validated_data,
            "message":"Streak created successfully"
        })


class StreakDetailView(APIView):
    queryset = Streak.objects.all()
    serializer_class = StreakDetailSerializer
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "body": serializer.data,
            "message":"Streak details retrieved successfully"
        })

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer( instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({ "status":"error", "body":{}, "message":"Invalid data" })
        return Response({
            "status": "success",
            "body": serializer.data,
            "message":"Streak updated successfully"
        })

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "status": "success",
            "body": {},
            "message":"Streak deleted successfully"
        })