from rest_framework import serializers
from streakify.streak_app.models import Streak, StreakRecord
from django.utils import timezone


class StreakRecordSerializer(serializers.ModelSerializer):
    streak_id = serializers.ReadOnlyField(source="streak.id")
    name = serializers.ReadOnlyField(source="streak.name")
    type = serializers.ReadOnlyField(source="streak.type")
    max_duration = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source="streak.created_by.id")
    user_started_from = serializers.SerializerMethodField()
    streak_started_from = serializers.SerializerMethodField()

    class Meta:
        model = StreakRecord
        fields = ['id', 'streak_id', 'name', 'type', 'max_duration', 'created_by',
                  'user_started_from', 'streak_started_from', 'punch_in']

    def get_max_duration(self, obj):
        if obj.streak.max_duration:
            return obj.streak.max_duration
        return None                  

    def get_user_started_from(self, obj):
        if obj.start_date:
            start_date = timezone.localtime(obj.start_date)
            return start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        return None

    def get_streak_started_from(self, obj):
        if obj.streak.start_date:
            start_date = timezone.localtime(obj.streak.start_date)
            return start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        return None


class StreakRecordMiniSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    name = serializers.ReadOnlyField(source='participant.name')
    user_id = serializers.ReadOnlyField(source='participant.id')
    country_code = serializers.ReadOnlyField(source='participant.user_profile.country.country_code')
    mobile_number = serializers.ReadOnlyField(source='participant.user_profile.mobile_number')
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = StreakRecord
        fields = [ 'user_id', 'name', 'country_code', 'mobile_number', 'profile_pic', 'punch_in', 'start_date' ]

    def get_profile_pic(self, obj):
        return obj.participant.user_profile.profile_pic.url if obj.participant.user_profile.profile_pic else ""


class StreakDetailSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    participants = StreakRecordMiniSerializer(source='streak_record', many=True)

    class Meta:
        model = Streak
        fields = [ 'id', 'name', 'type', 'max_duration', 'created_by', 'start_date',  'participants']



class StreakCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        model = Streak
        fields = ['id', 'name', 'type', 'max_duration', 'start_date', 'created_by']

    def to_internal_value(self, data):
        request = self.context.get("request")
        data["created_by"] = request.user.id
        return super().to_internal_value(data)
