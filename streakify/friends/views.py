from rest_framework.response import Response
from rest_framework.views import APIView
from streakify.friends.models import Friend
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from streakify.friends.serializers import FriendSerializer
from streakify.users.models import User, UserProfile
from rest_framework import status


class FriendsAPIView(ListCreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    
    def get_queryset(self):
        queryset = self.queryset.filter(server=self.request.user)
        status = self.request.GET.get("status") if "status" in self.request.GET else 1
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
        mobile_number = request.data.get("mobile_number") if "mobile_number" in request.data else None
        country_code =  request.data.get("country_code") if "country_code" in request.data else None
        if mobile_number and country_code:
            profile = UserProfile.objects.all().filter( mobile_number=mobile_number, country__country_code=country_code )
            if profile:
                user_ids = str(profile[0].user.id)
        user_ids = user_ids.split(",") if user_ids else []
        for user_id in user_ids:
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                except:
                    return Response({ "detail":"Invalid user_ids" }, status=status.HTTP_400_BAD_REQUEST)
                query = Friend.objects.all().filter( server=request.user, client=user, status=0 )
                if not query.exists(): 
                    friend = Friend.objects.create( server=request.user, client=user, status=0 )
                    friend.save()
        return Response({ "detail":"Friends added successfully" }, status=status.HTTP_201_CREATED)



class FriendRequestUpdateView(UpdateAPIView): 
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        print(request.data)
        serializer = self.get_serializer( instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({ "detail":"Invalid data" }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "body": serializer.data,
            "message":"Friend status updated successfully"
        })
