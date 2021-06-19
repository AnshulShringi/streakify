from rest_framework import serializers
from streakify.users.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    country_code = serializers.SerializerMethodField()
    mobile_number = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'country_code', 'mobile_number']

    def get_country_code(self, obj):
        profile = UserProfile.objects.filter(user=obj)
        if profile:
            return profile[0].country.country_code
        return ""

    def get_mobile_number(self, obj):
        profile = UserProfile.objects.filter(user=obj)
        if profile:
            return profile[0].mobile_number
        return ""