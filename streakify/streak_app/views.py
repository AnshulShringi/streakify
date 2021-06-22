from datetime import datetime
from rest_framework.response import Response
from streakify.streak_app.models import Streak, StreakRecord
from streakify.streak_app.serializers import StreakCreateSerializer, StreakRecordSerializer, StreakDetailSerializer
from rest_framework import status
from streakify.users.models import *
from rest_framework import generics
from datetime import datetime
from streakify.friends.models import Friend
from django.db.models import Q


class StreakListCreateView(generics.ListCreateAPIView):
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
        friends = request.data.pop('friends') if "friends" in request.data else None
        serializer = StreakCreateSerializer(data=request.data, context={'request':request})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({ "detail":"Invalid data" }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        friends_added = []
        for friend in friends:
            if Friend.objects.filter(Q(server=request.user, client=friend, status=1) | 
                                     Q(server=friend, client=request.user, status=1)):
                record = StreakRecord.objects.create(streak_id=serializer.data["id"], participant_id=friend)
                record.save()
                friends_added.append(friend)
        return Response({
            "body": {
                **serializer.data,
                "friends": friends_added,
            },
            "detail":"Streak created successfully"
        }, status=status.HTTP_201_CREATED)


class StreakDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Streak.objects.all()
    serializer_class = StreakDetailSerializer
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "body": serializer.data,
            "detail":"Streak fetched successfully"
        })

    def patch(self, request, *args, **kwargs):
        friends_data = request.data.pop("friends_record") if "friends_record" in request.data else None
        instance = self.get_object()
        serializer = self.get_serializer( instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({ "detail":"Invalid data" }, status=status.HTTP_400_BAD_REQUEST)
        
        for friend in friends_data:
            record = StreakRecord.objects.filter(streak=instance, participant_id=friend["user_id"])
            if friend["is_deleted"] and record.exists() and friend["user_id"] != record[0].streak.created_by.id:
                record.delete()
            elif not record.exists() and not friend["is_deleted"] and Friend.objects.filter(Q(server=request.user, client_id=friend["user_id"], status=1) | 
                Q(server_id=friend["user_id"], client=request.user, status=1)):
                new_record = StreakRecord.objects.create(streak=instance, participant_id=friend["user_id"])
                new_record.save()    
        serializer.save()            
        return Response({
            "detail":"Streak updated successfully"
        })

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "detail":"Streak deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class PunchInView(generics.UpdateAPIView):
    queryset = StreakRecord.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if not (instance.punch_in and instance.start_date):
            instance.start_date = datetime.now()
        instance.punch_in = True
        instance.save()
        return Response({ "detail": "Punched in successfully" })