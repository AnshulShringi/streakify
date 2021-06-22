from rest_framework import serializers
from streakify.friends.models import Friend


def get_friend_instance(user, obj):
    if obj.server == user:
        return obj.client
    return obj.server


class FriendListSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()
    mobile_number = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = ['id', 'user_id', 'name', 'email', 'country_code', 'mobile_number', 'profile_pic']

    def get_user_id(self, obj):
        request = self.context.get('request')
        instance = get_friend_instance(request.user, obj)
        return instance.id

    def get_name(self, obj):
        request = self.context.get('request')
        instance = get_friend_instance(request.user, obj)
        return instance.name if instance.name else ""

    def get_email(self, obj):
        request = self.context.get('request')
        instance = get_friend_instance(request.user, obj)
        return instance.email if instance.email else ""
    
    def get_country_code(self, obj):
        request = self.context.get('request')
        instance = get_friend_instance(request.user, obj)
        return instance.user_profile.country.country_code

    def get_mobile_number(self, obj):
        request = self.context.get('request')
        instance = get_friend_instance(request.user, obj)
        return instance.user_profile.mobile_number

    def get_profile_pic(self, obj):
        request = self.context.get('request')
        instance = get_friend_instance(request.user, obj)
        return instance.user_profile.profile_pic.url if instance.user_profile.profile_pic else ""


class FriendUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['status',]