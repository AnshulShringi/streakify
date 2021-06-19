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
        return None


class StreakCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streak
        fields = '__all__'

    def to_internal_value(self, data):
        request = self.context.get("request")
        data["created_by"] = request.user
        return super().to_internal_value(data)

    def create(self, validated_data, *args, **kwargs):
        request = self.context.get("request")
        user_ids = request.data.pop("user_ids") if "user_ids" in request.data else None
        user_ids = user_ids.split(",") if user_ids else []
        for user_id in user_ids:
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                except:
                    serializers 
                friend = StreakRecord.objects.create( status="pending", server=request.user, client=user )
                friend.save()

        obj = Streak.objects.create(**validated_data)
        obj.save()
        return obj


class StreakDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Streak
        fields = ["id", "name", "streak_type", "max_duration", "created_by"]