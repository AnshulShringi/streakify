from rest_framework import serializers
from streakify.users.models import User


class UserSerializer(serializers.ModelSerializer):
    country_code = serializers.ReadOnlyField(source='user_profile.country.country_code')
    mobile_number = serializers.ReadOnlyField(source='user_profile.mobile_number')
    profile_pic = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'country_code', 'mobile_number', 'name', 'email', 'profile_pic']

    def get_profile_pic(self, obj):
        if obj.user_profile.profile_pic:
            return obj.user_profile.profile_pic
        return None