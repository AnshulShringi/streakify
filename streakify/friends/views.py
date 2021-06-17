from rest_framework.response import Response
from rest_framework.views import APIView
from streakify.friends.models import Friend
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from streakify.friends.serializers import FriendSerializer
from streakify.users.models import User
from rest_framework import status


class FriendsAPIView(ListCreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    
    def get_queryset(self):
        queryset = self.queryset.filter(server=self.request.user)
        status = self.request.data.get("status") if "status" in self.request.data else None
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-created')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({ 
            "body":serializer.data, 
            "detail":"Data retrieved successfully" 
        })

    def post(self, request, *args, **kwargs):
        user_ids = request.data.get("user_ids") if "user_ids" in request.data else None
        user_ids = user_ids.split(",") if user_ids else []
        for user_id in user_ids:
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                except:
                    return Response({ "detail":"Invalid user_ids" }, status=status.HTTP_400_BAD_REQUEST) 
                friend = Friend.objects.create( status="pending", server=request.user, client=user )
                friend.save()
        return Response({ "detail":"Friends added successfully" }, status=status.HTTP_201_CREATED)



class FriendRequestUpdateView(UpdateAPIView): 
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer( instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({ "detail":"Invalid data" }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "body": serializer.data,
            "message":"Friend status updated successfully"
        })
