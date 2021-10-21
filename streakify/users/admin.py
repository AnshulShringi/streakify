# Core Django Imports
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Local Imports
from .models import User

UserSearchFields = [
    "id",
    "user__username",
    "user__email",
]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": (
                    "name",
                    "username",
                    "email",
                    "mobile_number",
                    "country_code",
                    "profile_pic",
                    "device_id",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "is_verified"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["id", "username", "mobile_number", "country_code", "is_verified"]
    search_fields = ["id", "name", "username", "mobile_number", "country_code"]
