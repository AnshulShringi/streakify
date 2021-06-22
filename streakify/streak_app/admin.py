from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from streakify.streak_app.models import Streak, StreakRecord


@admin.register(Streak)
class StreakAdmin(SimpleHistoryAdmin):
    model = Streak
    list_display = ["id", "name", "type", "max_duration","start_date", "created_by"]
    search_fields = ["name"]


@admin.register(StreakRecord)
class StreakRecordAdmin(SimpleHistoryAdmin):
    model = StreakRecord
    list_display = ["id", "streak", "start_date", "participant", "punch_in"]
    search_fields = ["name"]