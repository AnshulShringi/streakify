from rest_framework import serializers
from streakify.users.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    country_code = serializers.ReadOnlyField(source='user_profile.country.country_code')
    mobile_number = serializers.ReadOnlyField(source='user_profile.mobile_number')
    profile_pic = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'country_code', 'mobile_number', 'profile_pic']

    def get_profile_pic(self, obj):
        if obj.user_profile.profile_pic:
            return obj.user_profile.profile_pic.url
        return ""


class UserUpdateSerializer(serializers.ModelSerializer):
    profile_pic = serializers.FileField(required=False)
    
    class Meta:
        model = User
        fields = [ 'name', 'email', 'profile_pic' ]

    def update(self, instance, validated_data):
        profile_pic = validated_data.pop('profile_pic') if 'profile_pic' in validated_data else None
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        if profile_pic:
            profile = instance.user_profile
            profile.profile_pic = profile_pic
            profile.save()
        return instance