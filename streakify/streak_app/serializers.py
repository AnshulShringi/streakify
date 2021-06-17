from rest_framework import serializers
from streakify.streak_app.models import Streak, StreakRecord
from streakify.users.serializers import UserSerializer


class StreakListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="streak.id")
    name = serializers.ReadOnlyField(source="streak.name")
    streak_type = serializers.ReadOnlyField(source="streak.streak_type")
    max_duration = serializers.ReadOnlyField(source="streak.streak_type")
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = StreakRecord
        fields = ['id', 'name', 'streak_type', 'max_duration', 'created_by']

    def get_created_by(self, obj):
        if obj.streak.created_by:
            serializer = UserSerializer(obj.streak.created_by)
            return serializer.data 
        return {}


class StreakCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streak
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user 
        obj = Streak.objects.create(**validated_data)
        obj.save()
        return obj


class StreakDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Streak
        fields = ["id", "name", "streak_type", "max_duration", "created_by"]