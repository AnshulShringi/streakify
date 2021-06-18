from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from streakify.friends.models import Friend


@admin.register(Friend)
class StreakAdmin(SimpleHistoryAdmin):
    model = Friend
    list_display = ["id", "status", "server", "client"]
    search_fields = ["id", "status", "server", "client"]