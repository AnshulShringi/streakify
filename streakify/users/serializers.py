from rest_framework import serializers

from streakify.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "username",
            "email",
            "country_code",
            "mobile_number",
            "profile_pic",
            "is_verified",
            "device_id",
        ]
        read_only_fields = ["id", "country_code", "mobile_number"]


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "country_code", "mobile_number", "profile_pic"]
