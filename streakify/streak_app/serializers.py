from rest_framework import serializers
from streakify.streak_app.models import Streak, StreakRecord


class StreakRecordSerializer(serializers.ModelSerializer):
    streak_id = serializers.ReadOnlyField(source="streak.id")
    name = serializers.ReadOnlyField(source="streak.name")
    type = serializers.ReadOnlyField(source="streak.type")
    max_duration = serializers.SerializerMethodField()
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    start_date = serializers.SerializerMethodField()

    class Meta:
        model = StreakRecord
        fields = ['id', 'streak_id', 'name', 'type', 'max_duration', 'created_by', 'start_date', 'punch_in']

    def get_max_duration(self, obj):
        if obj.streak.max_duration:
            return obj.streak.max_duration
        return None

    def get_start_date(self, obj):
        if obj.start_date:
            return obj.start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        return ""


class StreakCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        model = Streak
        fields = ['id', 'name', 'type', 'max_duration', 'start_date', 'created_by']

    def to_internal_value(self, data):
        request = self.context.get("request")
        data["created_by"] = request.user.id
        return super().to_internal_value(data)
