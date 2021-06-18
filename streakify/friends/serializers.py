from rest_framework import serializers
from streakify.friends.models import Friend
from streakify.users.serializers import UserSerializer


class FriendSerializer(serializers.ModelSerializer):
    server = UserSerializer(read_only=True)
    client = UserSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = "__all__"
