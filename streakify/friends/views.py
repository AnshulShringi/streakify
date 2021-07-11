from rest_framework.response import Response
from streakify.friends.models import Friend
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from streakify.friends.serializers import *
from streakify.users.models import User
from rest_framework import status
from django.db.models import Q
from streakify.streak_app.models import StreakRecord
from firebase_admin import messaging


def send_notification(message, user):
    device_token = user.user_profile.device_token
    try:
        message = messaging.Message(
            notification = messaging.Notification(
                title = message["title"],
                body = message["body"]),
            token = device_token)
        messaging.send(message)
    except:
        pass



class FriendsAPIView(ListCreateAPIView):
    queryset = Friend.objects.all()
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        active = queryset.filter((Q(server=request.user) | Q(client=request.user)), status=1)
        pending = queryset.filter(client=request.user, status=0)
        active_data = FriendListSerializer(active, many=True, context={'request': request}).data 
        pending_data = FriendListSerializer(pending, many=True, context={'request': request}).data
        return Response({ 
            "body":{
                "active_friends": active_data,
                "pending_friends": pending_data
            }, 
            "detail":"Data retrieved successfully" 
        })

    def post(self, request, *args, **kwargs):
        mobile_number = request.data.get("mobile_number") if "mobile_number" in request.data else None
        country_code =  request.data.get("country_code") if "country_code" in request.data else None
        if mobile_number and country_code:
            try:
                client = User.objects.get(
                    user_profile__mobile_number=mobile_number, 
                    user_profile__country__country_code=country_code
                )
            except:
                return Response({ "detail":"User doesn't exists. Please invite your friend to streakify first" }, status=status.HTTP_400_BAD_REQUEST)
            if client==request.user:
                return Response({ "detail":"Invalid data" }, status=status.HTTP_400_BAD_REQUEST)
            query = Friend.objects.filter( server=request.user, client=client, status=0 )
            if not query.exists(): 
                friend = Friend.objects.create( server=request.user, client=client, status=0 )
                friend.save()
                message = {}
                message["title"] = "Friend Request"
                display_name = request.user.name if request.user.name else request.user.username
                message["body"] = display_name + " sent you a friend request"
                send_notification(message, client)
            return Response({ "detail":"Friend request sent successfully" }, status=status.HTTP_201_CREATED)
        return Response({ "detail":"mobile_number and country_code required" }, status=status.HTTP_400_BAD_REQUEST)


class FriendRequestUpdateView(UpdateAPIView): 
    queryset = Friend.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        request_status = request.data.get("status", None)
        if instance.status in [0,1] and request_status:
            if request_status==1:
                instance.status = request_status
                instance.save()
                message = {}
                message["title"] = "Friend Request"
                display_name = request.user.name if request.user.name else request.user.username
                message["body"] = display_name + " accepted your friend request"
                send_notification(message, instance.server)
                return Response({"message":"Friend request accepted successfully"})
            elif request_status==2:
                user1 = instance.server
                user2 = instance.client
                streak_record = StreakRecord.objects.filter(Q(participant=user1, streak__created_by=user2) |
                                                            Q(participant=user2, streak__created_by=user1))
                streak_record.delete()
                instance.delete()
                return Response({"message":"Friend request rejected/Friend removed successfully"})
        return Response({ "detail":"Invalid request" }, status=status.HTTP_400_BAD_REQUEST)
